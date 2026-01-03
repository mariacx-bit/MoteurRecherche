import pandas as pd
import numpy as np

class SearchEngine:
    def __init__(self, corpus):
        """
        corpus : objet de type Corpus.
        """
        self.corpus = corpus

        self.corpus.build_vocab()
        self.corpus.build_mat_TF()
        self.corpus.build_mat_TFxIDF()

    def search(self, query, k=10):
        """
        Retourne un DataFrame pandas avec les meilleurs résultats.
        """
        resultats = self.corpus.rechercher(query, k=k)

        data = [
            {
                "score": score,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
            }
            for doc, score in resultats
        ]

        df = pd.DataFrame(data, columns=["score", "titre", "auteur", "date", "url"])
        return df
