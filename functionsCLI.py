from components import GestionnaireTaches
from tools import demander_entier_entre, ajouter_extension_json, demander_chaine

gestionnaire = GestionnaireTaches()

def add_task():
    nom_tache = demander_chaine("Quelle tâche souhaitez-vous ajouter à la liste ? ")
    gestionnaire.ajouter_tache(nom_tache)
    print("Tâche ajoutée.")

def remove_task():
    if not gestionnaire.taches:
        print("Il n'y a pas de tâche à retirer.")
    else:
        valeur = demander_entier_entre(1, len(gestionnaire.taches))
        gestionnaire.supprimer_tache(valeur)
        print("Tâche supprimée.")

def change_state():
    if not gestionnaire.taches:
        print("Il n'y a pas de tâches à modifier.")
    else:
        valeur = demander_entier_entre(1, len(gestionnaire.taches))
        gestionnaire.basculer_etat(valeur)
        print("État de la tâche modifié.")

def save_tasks():
    nom_fichier = demander_chaine()
    nom_fichier_json = ajouter_extension_json(nom_fichier)
    gestionnaire.sauvegarder(nom_fichier_json)
    print(f"Sauvegarde effectuée dans '{nom_fichier_json}'.")

def load_file():
    nom_fichier = demander_chaine()
    nom_fichier_json = ajouter_extension_json(nom_fichier)
    if gestionnaire.charger(nom_fichier_json):
        print(f"Tâches chargées depuis '{nom_fichier_json}'.")
    else:
        print(f"Le fichier '{nom_fichier_json}' n'a pas été trouvé.")