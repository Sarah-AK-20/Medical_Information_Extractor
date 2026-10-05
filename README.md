# Extraction automatique des posologies dans un corpus médical (Unitex/GramLab)

## 1. Objectif du projet

Ce projet a pour but de repérer automatiquement, dans un corpus de textes médicaux en
français (comptes rendus hospitaliers, ordonnances, etc.), les expressions décrivant la
**posologie d'un médicament** — c'est-à-dire des séquences du type :

> *simvastatine 20 mg : 1‑0‑0*
> *INEXIUM 40 mg : 1 cp/j à 19 heures pendant un mois*

Pour cela, le projet s'appuie sur **Unitex/GramLab**, une plateforme de traitement
automatique des langues fondée sur des dictionnaires électroniques et des grammaires
locales représentées par des automates (graphes `.grf`).

La chaîne de traitement se décompose en deux grandes étapes :

1. **Construction d'un dictionnaire des substances actives** (noms de médicaments),
   à partir du site VIDAL puis enrichi directement à partir du corpus étudié.
2. **Repérage des posologies** dans le corpus grâce à une grammaire locale, puis
   génération d'un concordancier (`concord.html`) listant toutes les occurrences
   trouvées.

## 2. Vue d'ensemble de la chaîne de traitement

```
        VIDAL (pages HTML)
               │
               ▼
        extraire.py  ──────────────►  subst.dic  (+ infos1.txt)
               │
               ▼
   corpus-medical.txt (corpus à analyser)
               │
               ▼
        enrichir.py  ──────────────►  subst.dic enrichi
                                       subst_corpus.dic
                                       (+ infos2.txt, infos3.txt)
               │
               ▼
        unitex.py  (pilote les outils Unitex en ligne de commande)
               │
       ┌───────┴────────────────────────────────────────┐
       ▼                                                 ▼
  Normalize / Tokenize                         Compress subst.dic → subst.bin
  (corpus-medical.snt)                         Dico (application des dictionnaires)
       │                                                 │
       └───────────────────────┬─────────────────────────┘
                                ▼
                     Grf2Fst2  posologie.grf → posologie.fst2
                                │
                                ▼
                   Locate (repérage des posologies dans le corpus)
                                │
                                ▼
                   Concord   ──────────────►   concord.html
```

## 3. Description des fichiers

### `extraire.py`
Extrait les noms de médicaments (substances actives) depuis les pages HTML du
répertoire **VIDAL** (une page par lettre de l'alphabet, ex. `vidal-Sommaires-
Substances-A.htm`). Les liens `<a>...</a>` de chaque page sont parcourus, filtrés
selon la lettre attendue, puis normalisés (gestion des accents).

Sorties :
- `subst.dic` : dictionnaire électronique au format DELAF, encodé en **UTF‑16 LE**,
  où chaque entrée a la forme `nom,.N+subst` (nom commun, code grammatical N,
  trait sémantique `subst` = substance).
- `infos1.txt` : statistiques du nombre d'entités extraites par lettre.

Usage :
```bash
python extraire.py <dossier_VIDAL>
```

### `enrichir.py`
Complète le dictionnaire `subst.dic` avec les substances présentes dans le corpus
médical mais absentes du VIDAL (nouveaux noms, abréviations, variantes typographiques).
Une expression régulière repère les lignes du type *« nom_substance dose (mg/g/UI/…) »*
dans `corpus-medical.txt`.

Sorties :
- `subst_corpus.dic` : nouvelles substances trouvées dans le corpus.
- `subst.dic` (réécrit) : union du dictionnaire existant et des substances du corpus.
- `infos2.txt` : liste alphabétique complète des substances après enrichissement,
  avec un décompte par lettre.
- `infos3.txt` : liste des substances *ajoutées* (différence entre corpus et VIDAL),
  avec décompte par lettre.

Usage :
```bash
python enrichir.py [chemin_du_corpus]   # par défaut : corpus-medical.txt
```

### `posologie.grf`
Graphe Unitex/GramLab (format Unigraph, encodé en UTF‑16 BE) qui définit la
**grammaire locale de la posologie**. Il décrit l'enchaînement attendu des
composants d'une posologie :

- `<N+subst>` : nom de la substance (reconnu via le dictionnaire `subst.dic`)
- `dosage`
- `quantite et type`
- `frequence`
- `duree`
- `heure`

Ce graphe est compilé en automate (`.fst2`) puis utilisé par la commande `Locate`
pour rechercher toutes les occurrences de ce patron dans le corpus tokenisé.

### `unitex.py`
Script d'orchestration qui enchaîne les commandes en ligne de commande d'Unitex
(`UnitexToolLogger`) :

1. **Normalize** — normalise le texte brut (`corpus-medical.txt` → `corpus-medical.snt`).
2. **Tokenize** — découpe le texte en tokens, à l'aide de `Alphabet.txt`
   (fichier obligatoire décrivant les caractères de la langue et les
   correspondances minuscules/majuscules).
3. **Compress** — compile `subst.dic` en dictionnaire binaire `subst.bin`.
4. **Dico** — applique les dictionnaires (`subst.bin` + `Dela_fr.bin`, le
   dictionnaire du français) sur le corpus tokenisé.
5. **Grf2Fst2** — compile `posologie.grf` en automate `posologie.fst2`.
6. **Locate** — recherche toutes les correspondances du patron de posologie
   dans le corpus.
7. **Concord** — génère le concordancier final.

Usage :
```bash
python unitex.py
```

### `concord.html`
Concordancier généré par Unitex : chaque ligne montre une occurrence trouvée dans
son contexte gauche/droite, avec l'expression de posologie repérée mise en évidence
sous forme de lien (les coordonnées dans le lien correspondent aux positions dans
le corpus). Ce fichier est le **résultat final** du projet.

## 4. Prérequis

- **Unitex/GramLab** installé, avec l'exécutable `UnitexToolLogger` accessible
  dans le `PATH` (le script `unitex.py` utilise `os.system`, donc l'environnement
  doit être configuré au préalable — testé sous Windows).
- Un fichier `Alphabet.txt` (alphabet du français) et le dictionnaire `Dela_fr.bin`
  (dictionnaire DELAF du français), fournis par Unitex.
- Python 3 (aucune dépendance externe : `re`, `os`, `sys`, `unicodedata`).
- Le corpus à analyser, nommé `corpus-medical.txt` (encodage UTF‑8).
- Un dossier contenant les pages HTML du VIDAL (sommaire des substances par lettre).

## 5. Étapes d'exécution complètes

```bash
# 1. Construire le dictionnaire initial des substances à partir du VIDAL
python extraire.py chemin/vers/dossier_VIDAL

# 2. Enrichir ce dictionnaire avec les substances trouvées dans le corpus
python enrichir.py corpus-medical.txt

# 3. Lancer la chaîne Unitex (normalisation, dictionnaires, grammaire, concordance)
python unitex.py

# 4. Consulter le résultat
# → ouvrir concord.html dans un navigateur
```

## 6. Fichiers produits

| Fichier              | Généré par     | Contenu                                                        |
|-----------------------|----------------|------------------------------------------------------------------|
| `subst.dic`           | extraire.py / enrichir.py | Dictionnaire des substances (DELAF, UTF‑16 LE) |
| `subst_corpus.dic`    | enrichir.py    | Substances propres au corpus (avant fusion)                     |
| `infos1.txt`          | extraire.py    | Statistiques des substances extraites du VIDAL par lettre       |
| `infos2.txt`          | enrichir.py    | Liste complète des substances du corpus, par lettre             |
| `infos3.txt`          | enrichir.py    | Substances nouvellement ajoutées, par lettre                    |
| `corpus-medical.snt`  | unitex.py (Normalize) | Corpus normalisé                                          |
| `subst.bin`           | unitex.py (Compress)  | Dictionnaire compilé                                       |
| `posologie.fst2`      | unitex.py (Grf2Fst2)  | Grammaire de posologie compilée                             |
| `concord.html`        | unitex.py (Concord)   | Concordancier final des posologies repérées                 |

## 7. Remarques

- Les dictionnaires Unitex (`.dic`) doivent impérativement être encodés en
  **UTF‑16 LE avec BOM** pour être lus correctement par Unitex.
- Les graphes (`.grf`) sont encodés en **UTF‑16 BE**.
- Le champ sémantique `+subst` associé à chaque entrée du dictionnaire permet à la
  grammaire `posologie.grf` de reconnaître spécifiquement les noms de substances
  actives (via l'étiquette `<N+subst>`) et de les distinguer des autres noms communs
  du dictionnaire du français.
