
from tkinter import filedialog

from components import GestionnaireTaches, chargeWJson

gestionnaire = GestionnaireTaches()

def load_file_W():
    # Ouvre l'explorateur de fichiers
    filepath = filedialog.askopenfilename(
        title="Choisir un fichier",
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
    )
    chargeWJson(filepath)