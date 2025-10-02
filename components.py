import json
from tkinter import messagebox


class Tache:
    def __init__(self, nom, etat=False):
        self.nom = nom
        self.etat = etat  # False = en cours, True = terminé

    def basculer_etat(self):
        """Inverse l'état de la tâche"""
        self.etat = not self.etat

    def to_dict(self):
        """Convertit l'objet en dictionnaire JSON-serializable"""
        return {"nom": self.nom, "etat": self.etat}

    @staticmethod
    def from_dict(d):
        """Reconstruit une Tache depuis un dictionnaire"""
        return Tache(d["nom"], d["etat"])

    def __str__(self):
        """Représentation lisible de la tâche"""
        etat_texte = "terminé" if self.etat else "en cours"
        return f"{self.nom} - {etat_texte}"


class GestionnaireTaches:
    def __init__(self):
        self.taches = []

    def ajouter_tache(self, nom):
        self.taches.append(Tache(nom))

    def supprimer_tache(self, id_tache):
        self.taches.pop(id_tache - 1)

    def basculer_etat(self, id_tache):
        self.taches[id_tache - 1].basculer_etat()

    def display_tasks(self):
        if not self.taches:
            print("Aucune tâche enregistrée.")
        else:
            for i, tache in enumerate(self.taches, start=1):
                print(f"[{i}] {tache}")

    def sauvegarder(self, filename):
        data = [t.to_dict() for t in self.taches]
        sauvegardeSimpleJson(data, filename)

    def charger(self, filename):
        data = chargeSimpleJson(filename)
        self.taches = [Tache.from_dict(d) for d in data]


def sauvegardeSimpleJson(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def chargeSimpleJson(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            print(f"Chargement effectué depuis '{filename}'.")
            return json.load(f)
    except FileNotFoundError:
        print(f"Le fichier '{filename}' n'existe pas.")
        return []

def chargeWJson(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except UnicodeDecodeError:
        messagebox.showerror("Erreur", "Le fichier n'est pas compatible.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier n'existe pas.")
    except json.decoder.JSONDecodeError:
        messagebox.showerror("Erreur", "Le fichier semble illisible.")