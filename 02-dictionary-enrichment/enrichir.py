import re
from os import startfile
from sys import argv

# Vérifier si un chemin de fichier est fourni en tant qu'argument de ligne de commande
if(len(argv) == 2):
	path = argv[1]
else:  # Chemin de fichier par défaut s'il n'est pas fourni
	path = 'corpus-medical.txt'

# Créer et ouvrir le fichier pour le dictionnaire du corpus médical
dic_corpus = open('subst_corpus.dic', 'w', encoding="UTF-16 LE")
dic_corpus.write(u'\ufeff')

# Lire le dictionnaire existant des substances médicales
dic_temp = open('subst.dic', 'r', encoding="UTF-16 LE").read().replace(u'\ufeff', '').split("\n")
# Supprimer la ligne vide du résultat
if '' in dic_temp:
    dic_temp.remove('')
dic = {med[0:-9] for med in dic_temp}


ensemble_corpus = {} # Ensemble pour stocker les nouvelles substances médicales du corpus
# Définir le motif de recherche pour les substances médicales dans le corpus
pattern_substance = r'^[ 0-9\tØ-]*([A-Za-zéèê]{3,})( LP)?[ :]*?(\d+(\.\d+|,\d+)?|(un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)[ ])[ :]*?(mg|U[ ]|UI|g|µg|ml|[,: ]?[ ]?\d*?(/j|sachet(s)?))'
# Lire le contenu du fichier corpus médical
contenu_corpus = open(path, 'r', encoding="UTF-8").read().replace(u'\u00A0',' ')
# Trouver les substances médicales dans le corpus
subst = re.findall(pattern_substance, contenu_corpus, re.I | re.M)

# Écrire les nouvelles substances médicales dans le dictionnaire du corpus médical
for i in subst:
    dic_corpus.write(f'{i[0].lower()},.N+subst\n')
dic_corpus.close()
ensemble_corpus = {i[0].lower() for i in subst}
print('subst_corpus.dic est créé avec succès.')

# Fusionner le dictionnaire existant avec les nouvelles substances médicales du corpus
resultat_final_enrichir = list(dic.union(ensemble_corpus))
enrichissement = list(ensemble_corpus.difference(dic))
resultat_final_enrichir.sort()
enrichissement.sort()
# print(enrichissement)

# Ouvrir et écrire dans le dictionnaire après l'enrichissement
dic_apres_enrichissement = open('subst.dic', 'w', encoding="UTF-16 LE")
dic_apres_enrichissement.write(u'\ufeff')
for elt in resultat_final_enrichir:
    dic_apres_enrichissement.write(f'{elt},.N+subst\n')
dic_apres_enrichissement.close()
print('subst.dic est enrichi avec succès.')

# Générer le fichier infos2.txt
list_corpus = list(ensemble_corpus)
list_corpus.sort()

caractere_courant = 'a'
cmpt_lettre = 0
cmpt_total = 0
f2 = open('infos2.txt', 'w', encoding="UTF-8")
for i in list_corpus:
    while (caractere_courant != i[0]):
        f2.write("------------------------------------------\n")
        f2.write(f'Total de {caractere_courant.upper()} = {cmpt_lettre}\n')
        f2.write("------------------------------------------\n")
        caractere_courant = chr(ord(caractere_courant)+1)
        cmpt_total += cmpt_lettre
        cmpt_lettre = 0 
    f2.write(i+"\n")
    cmpt_lettre += 1

f2.write("------------------------------------------\n")
f2.write(f'{caractere_courant.upper()}: {cmpt_lettre}\n')
f2.write("------------------------------------------\n")
f2.write(f'Nombre total des substances actives = {cmpt_total}')
print('infos2.txt est généré avec succès.')
f2.close()


# Générer le fichier infos3.txt
caractere_courant = 'a'
cmpt_lettre = 0
cmpt_total = 0
f3 = open('infos3.txt', 'w', encoding="UTF-8")
for doc in enrichissement:
    while (caractere_courant != doc[0]):
        f3.write("------------------------------------------\n")
        f3.write(f'Total de {caractere_courant.upper()} = {cmpt_lettre}\n')
        f3.write("------------------------------------------\n")
        caractere_courant = chr(ord(caractere_courant)+1)
        cmpt_total += cmpt_lettre
        cmpt_lettre = 0 
    f3.write(doc+"\n")
    cmpt_lettre += 1
f3.write("------------------------------------------\n")
f3.write(f'Total de {caractere_courant.upper()} = {cmpt_lettre}\n')
f3.write("------------------------------------------\n")
f3.write(f'Nombre total des substances actives = {cmpt_total}')
print('infos3.txt est généré avec succès.')
f3.close()