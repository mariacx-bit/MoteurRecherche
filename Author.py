class Author:
    def __init__(self, name):
        self.name = name     
        self.production = [] 

    def add(self,document):
        self.production.append(document)
        
    def nb_docs(self):
        return len(self.production)
    
    def __str__(self):
        return f"{self.name} - {self.nb_docs()} document(s)"