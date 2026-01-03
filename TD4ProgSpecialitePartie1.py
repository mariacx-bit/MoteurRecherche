from datetime import datetime
import praw
import urllib.request
import xmltodict

from Document import RedditDocument, ArxivDocument
from Corpus import Corpus
from DocumentFactory import DocumentFactory
from SearchEngine import SearchEngine

theme = "healthy"
theme = "healthy"
documents = {}
doc_id = 1 

# Reddit 
reddit = praw.Reddit(
    client_id='JTK2goCuXWt80l2W8_8fpg',
    client_secret='BboDJ4bLTldUHpGuIV3MYT82MiUVfA',
    user_agent='MCScrapping'
)

subreddit = reddit.subreddit(theme)
for submission in subreddit.search(theme, limit=20):
    texte = submission.selftext.replace("\n", " ").strip()
    if texte:
        date_pub = datetime.utcfromtimestamp(submission.created_utc).strftime("%Y-%m-%d")
        doc_instance = RedditDocument(
            titre=submission.title,
            auteur=submission.author.name if submission.author else "Inconnu",
            date=date_pub,
            url=submission.url,
            texte=texte,
            nb_comments=submission.num_comments,
        )
        documents[doc_id] = doc_instance
        doc_id += 1

# ArXiv 
url = f"http://export.arxiv.org/api/query?search_query=all:{theme}&start=0&max_results=10"
try:
    with urllib.request.urlopen(url) as response:
        data = response.read()
    feed = xmltodict.parse(data)
    entries = feed['feed'].get('entry', [])
    if isinstance(entries, dict):
        entries = [entries]  

    for entry in entries:
        summary = entry.get('summary', '').replace("\n", " ").strip()
        if summary:
            date_pub = entry.get('published',datetime.now().strftime("%Y-%m-%d"))[:10]
            authors_field = entry.get('author', [])
            if isinstance(authors_field, list):
                principaux = (authors_field[0].get('name', 'Inconnu')
                              if authors_field else "Inconnu")
                co_auteurs = [a.get('name', 'Inconnu')
                              for a in authors_field[1:]]
            else:
                principaux = authors_field.get('name', 'Inconnu')
                co_auteurs = []
            doc_instance = ArxivDocument(
                titre=entry.get('title', f"Arxiv Doc {doc_id}"),
                auteur=principaux,
                date=date_pub,
                url=entry.get('id', ''),
                texte=summary,
                co_auteurs=co_auteurs,
            )
            documents[doc_id] = doc_instance
            doc_id += 1
except Exception as e:
    print("Erreur lors de l'accès à Arxiv:", e)

print(f"Total documents collected: {len(documents)}")

# Exemple
print(documents[2])
documents[2].infos_completes()

#TEST POLYMORPHISME 3.1 - 3.2
mon_corpus = Corpus("Corpus_Healthy")
mon_corpus.documents = documents
mon_corpus.id_document = len(documents)

print("\n Test polymorphisme : tri par date ")
mon_corpus.trier_par_date(5)

print("\n Test polymorphisme : tri par titre ")
mon_corpus.trier_par_titre(5)

print("\n Test polymorphisme : affichage avec source ")
mon_corpus.afficher_avec_source(10)

#Appel singleton
mon_corpus = Corpus.get_instance("Corpus_Healthy")
mon_corpus.documents = documents
mon_corpus.id_document = len(documents)

# Reddit
doc_instance = DocumentFactory.create_reddit(submission, date_pub, texte)

# Arxiv
doc_instance = DocumentFactory.create_arxiv(entry, date_pub, summary, principaux, co_auteurs)

mot = input("Mot-clé à chercher : ")
occurrences = mon_corpus.search(mot)

print(f"\nOccurrences de '{mot}' :")
for doc, extrait in occurrences[:10]:
    print(f"- {doc.titre} ({doc.date}) : ...{extrait}...")

mot = input("Mot-clé pour le concordancier : ")
df_conc = mon_corpus.concorde(mot, contexte=30)

print(df_conc[["contexte_gauche", "motif_trouve", "contexte_droit"]].head(5))
 
mon_corpus = Corpus("Corpus_Healthy")
mon_corpus.documents = documents
mon_corpus.id_document = len(documents)

moteur = SearchEngine(mon_corpus)

requete = input("\nRequête de recherche (mots-clés) : ")
df_res = moteur.search(requete, k=10)

print("\nRésultats de recherche :")
print(df_res.head(10))

requete = input("\nRequête de recherche (mots-clés) : ")
resultats = mon_corpus.rechercher(requete, k=10)

print("\nMeilleurs résultats :")
for doc, score in resultats:
    print(f"{score:.3f} | {doc.titre} ({doc.date})")

moteur = SearchEngine(mon_corpus)

requete = input("\nRequête de recherche (mots-clés) : ")
df_res = moteur.search(requete, k=10)

print("\nRésultats de recherche :")
print(df_res.head(10))
