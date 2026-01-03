import os
import pandas as pd
import praw
import urllib.request
import xmltodict

fichier_corpus = "corpus_healthy.csv"
theme = "healthy"

if os.path.exists(fichier_corpus):
    print(f" Chargement du corpus existant depuis '{fichier_corpus}'...")
    df = pd.read_csv(fichier_corpus, sep='\t')
    print(f" Corpus chargé ({len(df)} documents)") 
else:
    print(" Aucun corpus local trouvé. Collecte depuis les APIs Reddit et Arxiv...")

    # Reddit 
    reddit = praw.Reddit(
        client_id='JTK2goCuXWt80l2W8_8fpg',
        client_secret='BboDJ4bLTldUHpGuIV3MYT82MiUVfA',
        user_agent='MCScrapping'
    )

    docs = []
    sources = []

    print("🔹 Collecte depuis Reddit...")
    subreddit = reddit.subreddit(theme)
    for submission in subreddit.search(theme, limit=20):
        texto = submission.selftext.replace("\n", " ").strip()
        if texto:
            docs.append(texto)
            sources.append("Reddit")

    # Arxiv 
    print("🔹 Collecte depuis Arxiv...")
    url = f"http://export.arxiv.org/api/query?search_query=all:{theme}&start=0&max_results=10"

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
        feed = xmltodict.parse(data)
        entries = feed['feed'].get('entry', [])
        if isinstance(entries, list):
            for entry in entries:
                summary = entry.get('summary', '')
                if summary:
                    docs.append(summary.replace("\n", " ").strip())
                    sources.append("Arxiv")
        elif isinstance(entries, dict):
            summary = entries.get('summary', '')
            if summary:
                docs.append(summary.replace("\n", " ").strip())
                sources.append("Arxiv")
    except Exception as e:
        print("Erreur lors de l'accès à Arxiv:", e)

    df = pd.DataFrame({
        "id": range(1, len(docs) + 1),
        "texte": docs,
        "source": sources
    })

    df.to_csv(fichier_corpus, sep="\t", index=False, encoding="utf-8")
    print(f"💾 Corpus sauvegardé sous '{fichier_corpus}' avec tabulations comme séparateur.")

print("\n Aperçu du corpus :")
print(df.head())

df['nb_mots'] = df['texte'].apply(lambda x: len(x.split()))
df['nb_phrases'] = df['texte'].apply(lambda x: len(x.split('.')))
print(df[['texte', 'nb_mots', 'nb_phrases']].head())

df = df[df['texte'].str.len() >= 100]
print(f" Nombre de documents après suppression : {len(df)}")

corpus_texte = ' '.join(df['texte'].tolist())
print(f" Longueur totale du corpus : {len(corpus_texte)} caractères")
print(f" Aperçu : {corpus_texte[:500]}...")  
