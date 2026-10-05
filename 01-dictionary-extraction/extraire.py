import os
import re
import sys
import unicodedata

def normaliser_lettre(lettre):
    """Normalise une lettre pour ignorer les accents."""
    return unicodedata.normalize('NFD', lettre).encode('ascii', 'ignore').decode('utf-8')

def extraire_noms_medicaments(fichier_html, lettre_cible):
    """Extrait les noms de médicaments d'un fichier HTML en filtrant par la lettre donnée"""
    noms = []
    with open(fichier_html, 'r', encoding='utf-8') as f:
        content = f.read()

        # Recherche des sections contenant les médicaments par lettre
        pattern = re.compile(r'<a[^>]*>([^<]+)</a>', re.S)
        matches = pattern.findall(content)

        # Filtrer les médicaments qui commencent par la lettre cible
        for match in matches:
            médicament = match.strip()
            # Vérifier si le médicament commence par la lettre cible ou une variante avec accents
            if médicament and normaliser_lettre(médicament[0].lower()) == normaliser_lettre(lettre_cible.lower()) and len(médicament) > 1 and médicament[0].islower():
                noms.append(médicament)
    
    return noms

def creer_dictionnaire_alfabetique(noms_medicaments):
    """Crée un dictionnaire des médicaments organisés par lettre"""
    dictionnaire = {}
    for nom in noms_medicaments:
        premiere_lettre = normaliser_lettre(nom[0].lower())
        if premiere_lettre not in dictionnaire:
            dictionnaire[premiere_lettre] = []
        dictionnaire[premiere_lettre].append(f"{nom},.N+subst")
    return dictionnaire

def generer_delf(noms_medicaments, fichier_sortie):
    """Génère un fichier DELAF avec les médicaments"""
    with open(fichier_sortie, 'w', encoding='utf-16-le') as f:
        # Écrire un BOM (byte-order mark) pour UTF-16 LE
        f.write('\ufeff')
        for nom in noms_medicaments:
            f.write(f"{nom},.N+subst\n")

def generer_infos(dictionnaire, fichier_infos):
    """Génère le fichier infos1.txt avec les statistiques"""
    with open(fichier_infos, 'w', encoding='utf-8') as f:
        total_entites = 0
        for lettre, mots in sorted(dictionnaire.items()):
            nombre = len(mots)
            f.write(f"{lettre.upper()} : {nombre} entités\n")
            total_entites += nombre
        f.write(f"Total : {total_entites} entités\n")

def traiter_dossier_vidal(dossier_vidal):
    """Traite tous les fichiers HTML dans le dossier VIDAL"""
    noms_medicaments = []

    # Parcourir tous les fichiers HTML dans le dossier VIDAL
    for fichier in os.listdir(dossier_vidal):
        if fichier.endswith('.htm') or fichier.endswith('.html'):
            # Extraire la lettre cible du nom du fichier
            lettre_cible = fichier.split('-')[-1][0].lower()  # Par exemple, 'A' à partir de 'vidal-Sommaires-Substances-A.htm'
            
            chemin_fichier = os.path.join(dossier_vidal, fichier)
            noms_medicaments += extraire_noms_medicaments(chemin_fichier, lettre_cible)

    # Créer un dictionnaire alphabétique des médicaments
    dictionnaire = creer_dictionnaire_alfabetique(noms_medicaments)

    # Générer le fichier DELAF
    generer_delf(noms_medicaments, 'subst.dic')

    # Générer le fichier infos1.txt
    generer_infos(dictionnaire, 'infos1.txt')

    # Afficher les statistiques dans la console
    for lettre, mots in sorted(dictionnaire.items()):
        print(f"{lettre.upper()} : {len(mots)} entités")
    total = sum(len(mots) for mots in dictionnaire.values())
    print(f"Total : {total} entités")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <dossier_vidal>")
        sys.exit(1)

    dossier_vidal = sys.argv[1]

    if not os.path.isdir(dossier_vidal):
        print(f"Erreur : le dossier {dossier_vidal} n'existe pas.")
        sys.exit(1)

    traiter_dossier_vidal(dossier_vidal)
    print("Extraction terminée. Fichiers 'subst.dic' et 'infos1.txt' générés.")
