from functionsCLI import add_task, change_state, remove_task, load_file, save_tasks, gestionnaire
from tools import checkIntBetweenXandY

menu = {
    1: load_file,
    2: gestionnaire.display_tasks,
    3: add_task,
    4: change_state,
    5: remove_task,
    6: save_tasks,
    7: exit
}

def mainCLI():

    while True:
        print("""
        Menu principal : 
        1. Charger les tâches depuis un fichier
        2. Afficher les tâches
        3. Ajouter une nouvelle tâche
        4. Marquer une tâche comme terminée / en cours
        5. Supprimer une tâche
        6. Sauvegarder les tâches actuelles
        7. Quitter
        """)

        key = checkIntBetweenXandY(1, 7)

        if key in menu:
            menu[key]()



if __name__ == "__main__":
    mainCLI()