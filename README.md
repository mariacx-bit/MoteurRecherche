# Moteur de recherche – Discours politiques US

Ce dépôt contient le projet de moteur de recherche développé dans le cadre du cours de Programmation de spécialité (Master 1 Informatique, 2025–2026). [file:516]

L’application permet d’explorer un corpus de discours politiques américains (2015–2016) :
- recherche par mots-clés avec score de pertinence ;
- filtrage par auteur et par année ;
- Analyse temporelle d’un terme (avant/après une année de référence). 

## Structure du projet

- `TD_discours_US.ipynb` : notebook principal servant d’interface utilisateur (ipywidgets).
- `discours_US.csv` : corpus de discours politiques US.   
- `rapport_projet.pdf` : rapport du projet (resume functionel du projet).   
- autres fichiers `.py` : classes et fonctions métier (Document, Corpus, SearchEngine, etc.). 

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/mariacx-bit/MoteurRecherche.git
   cd MoteurRecherche
# MoteurRecherche
