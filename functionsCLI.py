from components import GestionnaireTaches
from tools import checkIntBetweenXandY, checkExtensionJson, checkString

gestionnaire = GestionnaireTaches()

def add_task():
    gestionnaire.ajouter_tache(input("Quelle tache souhaitez-vous ajouter à la liste ?"))

def remove_task():
    if len(gestionnaire.taches) == 0:
        print("Il n'y a pas de tâche à retirer.")
    else:
        valeur = checkIntBetweenXandY(1, len(gestionnaire.taches))
        gestionnaire.supprimer_tache(valeur)

def change_state():
    if len(gestionnaire.taches) == 0:
        print("Il n'y a pas de tâches à modifier.")
    else:
        valeur = checkIntBetweenXandY(1, len(gestionnaire.taches))
        gestionnaire.basculer_etat(valeur)

def save_tasks():
    raw = checkString()
    fname = checkExtensionJson(raw)
    gestionnaire.sauvegarder(fname)
    print(f"Sauvegarde effectuée dans '{fname}'.")

def load_file():
    raw = checkString()
    fname = checkExtensionJson(raw)
    gestionnaire.charger(fname)

