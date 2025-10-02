import tkinter as tk

from functionsTKINTER import gestionnaire, load_file_W

root = tk.Tk()
root.title("Gestionnaire de tâches")
root.geometry("400x300")
root.resizable(False, False)

# Création d'une barre de menus
menubar = tk.Menu(root)

# Création d'un menu "Fichier"
menu_fichier = tk.Menu(menubar, tearoff=0)  # tearoff=0 empêche la séparation
menu_fichier.add_command(label="Charger", command=load_file_W)
menu_fichier.add_command(label="Sauvegarder", command=gestionnaire.ajouter_tache)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=exit)

# Ajout du menu "Fichier" dans la barre
menubar.add_cascade(label="Fichier", menu=menu_fichier)

# On attache la barre de menus à la fenêtre
root.config(menu=menubar)




root.mainloop()