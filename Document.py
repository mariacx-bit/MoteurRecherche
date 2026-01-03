# Creation de la classe Document (partie 1.1)
class Document:
    def __init__(self, titre, auteur, date, url, texte, champ_digest="titre",type_source="Generic"):
        self.titre = titre     
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.champ_digest = champ_digest 
        self.type = type_source

    # Méthode pour afficher toutes les informations (partie 1.2)
    def infos_completes(self):
        print(f"Titre : {self.titre}")
        print(f"Auteur : {self.auteur}")
        print(f"Date : {self.date}")  
        print(f"Url : {self.url}")
        print(f"Texte : {self.texte}")

    # Méthode __str__  version digeste (partie 1.2)
    def __str__(self):
        valeur = getattr(self, self.champ_digest, "Champ invalide")
        return f"{self.champ_digest.capitalize()}: {valeur}"
    def getType(self):
        return self.type

# TD5 - Partie 1 : classe fille RedditDocument
class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_comments, champ_digest="titre"):
        super().__init__(titre, auteur, date, url, texte, champ_digest,type_source="Reddit")
        self.nb_comments = nb_comments    

    def get_nb_comments(self):
        return self.nb_comments

    def set_nb_comments(self, nb):
        self.nb_comments = nb

    def __str__(self):
        base = super().__str__()   
        return f"[Reddit] {base} | Commentaires : {self.nb_comments}"

class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_auteurs=None, champ_digest="titre"):
        super().__init__(titre, auteur, date, url, texte, champ_digest,type_source="Arxiv")
        self.co_auteurs = co_auteurs if co_auteurs is not None else []

    def get_co_auteurs(self):
        return self.co_auteurs

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def __str__(self):
        base = super().__str__()  
        co = ", ".join(self.co_auteurs) if self.co_auteurs else "Aucun co-auteur"
        return f"[Arxiv] {base} | Co-auteurs : {co}"
