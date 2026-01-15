# Moteur de recherche – Discours politiques US

Ce dépôt contient le projet de moteur de recherche développé dans le cadre du cours de Programmation de spécialité (Master 1 Informatique, 2025–2026).

L’application permet d’explorer un corpus :
- recherche par mots-clés avec score de pertinence ;
- filtrage par auteur et par année ;
- Analyse temporelle d’un terme (avant/après une année de référence). 

## Structure du projet

- `TD_discours_US.ipynb` : notebook principal servant d’interface utilisateur (ipywidgets).
- `discours_US.csv` : corpus de discours politiques US.   
- `rapport_projet.pdf` : rapport du projet (resume functionel du projet).   
- autres fichiers `.py` : classes et fonctions métier (Document, Corpus, SearchEngine, etc.). 

## Installation et lancement
## Prérequis
- Python **3.x**
- Jupyter Notebook
- `pip` (gestionnaire de paquets Python)
- Git (pour cloner le dépôt)

# Cloner le dépôt
```bash
git clone https://github.com/mariacx-bit/MoteurRecherche.git
cd MoteurRecherche 
``` 
# Installation des dépendances
Si le fichier requirements.txt est présent :
```bash
pip install -r requirements.txt
``` 
Sinon, installer manuellement les principales dépendances utilisées dans le projet :
```bash
pip install pandas numpy scipy ipywidgets tqdm praw xmltodict
``` 
Sur Jupyter, il peut être nécessaire d’activer ipywidgets :
```bash
jupyter nbextension enable --py widgetsnbextension
``` 
### Lancer l’interface
```bash
jupyter notebook
```
# MoteurRecherche
