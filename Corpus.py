import re
import pandas as pd
from Document import Document
from collections import Counter
from scipy import sparse
import numpy as np
from numpy.linalg import norm
from tqdm import tqdm

class Corpus:
    _instance = None   # --- Singleton ---

    def __init__(self, nom):
        self.nom = nom
        self.documents = {}
        self.id_document = 0
        self.authors = {}
        self._texte_concatene = None
        self._index_docs = [] 
        self.doc_normes = None

    @classmethod
    def get_instance(cls, nom="Corpus_Healthy"):
        if cls._instance is None:
            cls._instance = cls(nom)
        return cls._instance

    @staticmethod
    def nettoyer_texte(texte: str) -> str:
        """Nettoyage de la chaîne."""
        
        t = texte.lower()
        
        t = t.replace("\n", " ")
        
        t = re.sub(r"[^a-zàâäéèêëîïôöùûüç\s]", " ", t)
       
        t = re.sub(r"\s+", " ", t).strip()
        return t
    # ---------- méthodes de tri ----------

    def trier_par_date(self, n):
        docs_tries = sorted(
            self.documents.values(),
            key=lambda d: d.date,
            reverse=True
        )
        print(f"\n{n} documents les plus recents du corps '{self.nom}':")
        for doc in docs_tries[:n]:
            print(f"- {doc.date} | {doc.titre} | {doc.auteur}")

    def trier_par_titre(self, n):
        docs_tries = sorted(
            self.documents.values(),
            key=lambda d: d.titre.lower()
        )
        print(f"\n{n} documents tries par le titre dans le corps '{self.nom}':")
        for doc in docs_tries[:n]:
            print(f"- {doc.titre} | {doc.date} | {doc.auteur}")

    def __repr__(self):
        return (
            f"Corpus: {self.nom}\n"
            f"Nombre de documents: {len(self.documents)}\n"
            f"Nombre d'auteurs: {len(self.authors)}"
        )

    # ---------- 3.3 : sauvegarde / chargement ----------

    def save_csv(self, path="corpus_healthy.csv"):
        df = pd.DataFrame([
            {
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
            }
            for doc_id, doc in self.documents.items()
        ])
        df.to_csv(path, sep="\t", index=False, encoding="utf-8")
        print(f"\nCorpus '{self.nom}' sauvegardé dans {path}")

    @classmethod
    def load_csv(cls, path="corpus_healthy.csv", nom="Corpus_Healthy_Loaded"):
        try:
            df = pd.read_csv(path, sep="\t", encoding="utf-8")
        except FileNotFoundError:
            print(f"Fichier CSV '{path}' non trouvé.")
            return None

        corpus = cls.get_instance(nom)
        for _, row in df.iterrows():
            doc = Document(
                titre=row["titre"],
                auteur=row["auteur"],
                date=row["date"],
                url=row["url"],
                texte=row["texte"],
            )
            corpus.id_document += 1
            corpus.documents[corpus.id_document] = doc

        print(f"Corpus '{corpus.nom}' chargé depuis {path} ({len(corpus.documents)} documents)")
        return corpus

    # ---------- 3.2 : affichage avec source ----------

    def afficher_avec_source(self, n=None):
        docs = list(self.documents.values())
        if n is not None:
            docs = docs[:n]
        for doc in docs:
            print(f"[{doc.getType()}] {doc.titre} | {doc.auteur} | {doc.date}")

    def _build_concatenated_text(self):
        """Construit une grande chaîne avec tous les textes et un index de positions."""
        if self._texte_concatene is not None:
            return

        morceaux = []
        self._index_docs = []
        pos = 0
        for doc_id, doc in self.documents.items():
            txt = doc.texte
            debut = pos
            fin = pos + len(txt)
            morceaux.append(txt)
            self._index_docs.append((doc_id, debut, fin))
            pos = fin + 1 
            morceaux.append("\n")  

        self._texte_concatene = "".join(morceaux)
        
    def search(self, motif):
        """
        Retourne les passages contenant motif regex..
        """
        if self._texte_concatene is None:
            self._build_concatenated_text()

        pattern = re.compile(motif, re.IGNORECASE)
        resultats = []

        for m in pattern.finditer(self._texte_concatene):
            start = m.start()
            end = m.end()

            for doc_id, debut, fin in self._index_docs:
                if debut <= start < fin:
                    doc = self.documents[doc_id]
                    local_start = max(0, start - debut - 30)
                    local_end = min(fin - debut, end - debut + 30)
                    extrait = doc.texte[local_start:local_end]
                    resultats.append((doc, extrait))
                    break

        return resultats
    def concorde(self, motif, contexte=30):
        """
        Construit un concordancier pour 'motif'.
        """
        if self._texte_concatene is None:
            self._build_concatenated_text()

        pattern = re.compile(motif, re.IGNORECASE)
        lignes = []

        for m in pattern.finditer(self._texte_concatene):
            start = m.start()
            end = m.end()

            for doc_id, debut, fin in self._index_docs:
                if debut <= start < fin:
                    doc = self.documents[doc_id]

                    local_start = start - debut
                    local_end = end - debut

                    gauche = doc.texte[max(0, local_start - contexte):local_start]
                    centre = doc.texte[local_start:local_end]
                    droit = doc.texte[local_end:local_end + contexte]

                    lignes.append({
                        "contexte_gauche": gauche,
                        "motif_trouve": centre,
                        "contexte_droit": droit,
                        "titre": doc.titre,      
                        "date": doc.date,
                    })
                    break

        df = pd.DataFrame(lignes, columns=["contexte_gauche", "motif_trouve", "contexte_droit", "titre", "date"])
        return df
    def stats(self, n=20):
        vocab = self.build_vocab()

        print(f"Nombre de mots différents dans le corpus : {len(vocab)}")

        compteur = {mot: infos["term_freq"] for mot, infos in vocab.items()}

        print(f"\n{n} mots les plus fréquents :")
        for mot, freq in sorted(compteur.items(), key=lambda x: x[1], reverse=True)[:n]:
            print(f"{mot} : {freq}")

        df_freq = pd.DataFrame(
            [
                {
                    "mot": mot,
                    "term_freq": infos["term_freq"],   
                    "doc_freq": infos["doc_freq"],     
                }
                for mot, infos in vocab.items()
            ]
        ).sort_values(by="term_freq", ascending=False).reset_index(drop=True)

        return df_freq

    def build_vocab(self):
        """
        Vocabulaire du corpus avec fréquences.
        """
        from collections import Counter

        doc_freq = Counter()
        term_freq = Counter()

        for doc in self.documents.values():
            texte_propre = self.nettoyer_texte(doc.texte)
            mots = texte_propre.split()

            term_freq.update(mots)

            doc_freq.update(set(mots))

        mots_tries = sorted(doc_freq.keys())

        vocab = {}
        for idx, mot in enumerate(mots_tries):
            vocab[mot] = {
                "id": idx,
                "doc_freq": doc_freq[mot],
                "term_freq": term_freq[mot],
            }

        self.vocab = vocab
        return vocab
    
    def build_mat_TF(self):
        """
        Construit la matrice Term Frequency (mat_TF).
        """
        if not hasattr(self, "vocab"):
            self.build_vocab()

        nb_docs = len(self.documents)
        nb_mots = len(self.vocab)

        rows = []
        cols = []
        data = []

    def build_mat_TF(self):
        """
        Construit la matrice Term Frequency (mat_TF).
        """
        if not hasattr(self, "vocab"):
            self.build_vocab()

        nb_docs = len(self.documents)
        nb_mots = len(self.vocab)

        rows = []
        cols = []
        data = []

        for i, (doc_id, doc) in tqdm(enumerate(self.documents.items()),
            total=nb_docs,
            desc="Construction mat_TF"):
            texte_net = self.nettoyer_texte(doc.texte)
            mots = texte_net.split()
            compteur = Counter(mots)

            for mot, tf in compteur.items():
                if mot in self.vocab:
                    j = self.vocab[mot]["id"]
                    rows.append(i)
                    cols.append(j)
                    data.append(tf)

        self.mat_TF = sparse.csr_matrix(
            (data, (rows, cols)), shape=(nb_docs, nb_mots), dtype=np.int32)

        return self.mat_TF
    
    def remplir_vocab_depuis_mat_TF(self):
        """
        Met à jour term_freq et doc_freq dans self.vocab depuis mat_TF.
        """
        if not hasattr(self, "mat_TF"):
            self.build_mat_TF()

        if not hasattr(self, "vocab"):
            self.build_vocab()

        mat = self.mat_TF 

        term_freqs = np.array(mat.sum(axis=0)).ravel()

        doc_freqs = np.array((mat > 0).sum(axis=0)).ravel()

        for mot, infos in self.vocab.items():
            j = infos["id"]             
            infos["term_freq"] = int(term_freqs[j])
            infos["doc_freq"] = int(doc_freqs[j])
    def build_mat_TFxIDF(self):
        """
        Construit la matrice TF×IDF (mat_TFxIDF).
        """
        if not hasattr(self, "mat_TF"):
            self.build_mat_TF()
        if not hasattr(self, "vocab"):
            self.build_vocab()

        mat = self.mat_TF.tocsr()        
        nb_docs, nb_mots = mat.shape

        doc_freqs = np.zeros(nb_mots, dtype=float)
        for mot, infos in self.vocab.items():
            j = infos["id"]
            doc_freqs[j] = infos["doc_freq"]

        doc_freqs[doc_freqs == 0] = 1.0

        idf = np.log(nb_docs / doc_freqs)

        self.mat_TFxIDF = mat.multiply(idf)
        self.doc_normes = np.sqrt(
        self.mat_TFxIDF.multiply(self.mat_TFxIDF).sum(axis=1)
        ).A1

        return self.mat_TFxIDF

    def _vector_query_TFxIDF(self, query):
        """
        Transforme une requête texte en vecteur TF×IDF.
        """
        if not hasattr(self, "mat_TFxIDF"):
            self.build_mat_TFxIDF()

        texte_net = self.nettoyer_texte(query)
        mots = texte_net.split()

        compteur = Counter(mots)

        nb_docs, nb_mots = self.mat_TFxIDF.shape
        vec = np.zeros(nb_mots, dtype=float)

        for mot, tf in compteur.items():
            if mot in self.vocab:
                j = self.vocab[mot]["id"]
                # IDF du mot j
                df = self.vocab[mot]["doc_freq"] or 1
                idf = np.log(nb_docs / df)
                vec[j] = tf * idf

        return vec
    
    def rechercher(self, query, k=10):
        """
        Retourne les k documents les plus proches de la requête.
        """
        if not hasattr(self, "mat_TFxIDF"):
            self.build_mat_TFxIDF()

        q = self._vector_query_TFxIDF(query)          
        if norm(q) == 0:
            return []

        scores = self.mat_TFxIDF.dot(q)             

        doc_normes = self.doc_normes
        scores = scores / (doc_normes * norm(q) + 1e-12)

        idx_tries = np.argsort(-scores)[:k]
        docs_list = list(self.documents.values())
        resultats = [(docs_list[i], float(scores[i])) for i in idx_tries]

        return resultats
