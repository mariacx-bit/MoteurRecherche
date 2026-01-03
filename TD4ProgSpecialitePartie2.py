from Author import Author  
from TD4ProgSpecialitePartie1 import documents
from Corpus import Corpus

authors ={} 

for doc_id, doc_instance in documents.items():
    for author_name in [a.strip() for a in doc_instance.auteur.split(",")]:
        if author_name not in authors:
            authors[author_name] = Author(author_name)
        authors[author_name].add(doc_instance)

for author in authors.values():
    print(author)
   
# ----------------- Statistiques pour un auteur donné -----------------
nom_recherche = input("Entrez le nom de l'auteur pour afficher ses statistiques : ").strip()

if nom_recherche in authors:
    auteur = authors[nom_recherche]
    nb_docs = auteur.nb_docs()
    
    tailles = [len(doc.texte) for doc in auteur.production]
    taille_moyenne = sum(tailles) / len(tailles) if tailles else 0

    print(f"\nAuteur : {auteur.name}")
    print(f"Nombre de documents : {nb_docs}")
    print(f"Taille moyenne des documents : {taille_moyenne:.2f} caractères")
else:
    print(f"\nAuteur '{nom_recherche}' non trouvé dans la base.")

# ----------------- Création du Corpus et sauvegarde/chargement  -----------------

mon_corpus = Corpus("Corpus_Healthy")
mon_corpus.documents = documents         
mon_corpus.authors = authors              
mon_corpus.id_document = len(documents)  

mon_corpus.save_csv("corpus_healthy.csv")

corpus_charge = Corpus.load_csv("corpus_healthy.csv", nom="Corpus_Healthy_Loaded")

if corpus_charge is not None:
    print("\n--- Aperçu du corpus chargé ---")
    print(corpus_charge)
    print(f"Nombre de documents : {len(corpus_charge.documents)}")
    

