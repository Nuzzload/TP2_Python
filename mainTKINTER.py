import tkinter as tk
from tkinter import ttk
import functionsTKINTER as ft

def main_tkinter():
    """Crée et lance l'interface graphique du gestionnaire de tâches."""
    root = tk.Tk()
    root.title("Gestionnaire de tâches")
    root.geometry("600x550")
    root.configure(bg="#F0F0F0")

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("Treeview",
                    background="#FFFFFF",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#FFFFFF")
    style.map('Treeview', background=[('selected', '#BDD5EF')])

    style.configure("TButton",
                    padding=6,
                    font=('Helvetica', 10),
                    relief="solid",
                    borderwidth=1)
    style.map("TButton",
              bordercolor=[('active', '#3399FF')],
              relief=[('pressed', 'sunken')])

    # Cadre pour la liste des tâches
    list_frame = ttk.Frame(root, padding="20 10 20 10")
    list_frame.pack(fill="both", expand=True)
    list_frame.grid_rowconfigure(0, weight=1)
    list_frame.grid_columnconfigure(0, weight=1)

    # "Arbre" pour afficher les tâches
    tree = ttk.Treeview(list_frame, columns=("state", "name"), show="headings", height=10)
    tree.heading("state", text="État")
    tree.heading("name", text="Tâche")
    tree.column("state", width=100, anchor="center")
    tree.column("name", width=350)
    tree.grid(row=0, column=0, sticky="nsew")
    tree.bind("<Double-1>", ft.basculer_etat_double_clic)
    tree.bind("<Motion>", ft.gerer_mouvement_tree)
    tree.bind("<Leave>", ft.gerer_sortie_tree)

    # Barre de défilement
    y_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    tree.config(yscrollcommand=y_scrollbar.set)

    # Cadre pour l'ajout de tâches
    add_frame = ttk.Frame(root, padding="20 10 20 10")
    add_frame.pack(fill="x")

    task_entry = ttk.Entry(add_frame, font=('Helvetica', 11))
    task_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))

    add_button = ttk.Button(add_frame, text="Ajouter", command=lambda: ft.ajouter_tache_ihm(task_entry, tree))
    add_button.pack(side=tk.RIGHT)

    # Cadre pour les boutons d'action
    action_frame = ttk.Frame(root, padding="20 10 20 20")
    action_frame.pack(fill="x")

    toggle_button = ttk.Button(action_frame, text="Changer État", command=lambda: ft.basculer_etat_ihm(tree))
    toggle_button.pack(side=tk.LEFT, expand=True, padx=5)

    delete_button = ttk.Button(action_frame, text="Supprimer", command=lambda: ft.supprimer_tache_ihm(tree))
    delete_button.pack(side=tk.LEFT, expand=True, padx=5)

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    menu_fichier = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Fichier", menu=menu_fichier)

    menu_fichier.add_command(label="Sauvegarder", command=ft.sauvegarder_fichier)
    menu_fichier.add_command(label="Charger", command=lambda: ft.charger_fichier(tree))
    menu_fichier.add_separator()
    menu_fichier.add_command(label="Quitter", command=root.quit)

    # Premier affichage
    ft.mettre_a_jour_liste_taches(tree)
    root.mainloop()

if __name__ == "__main__":
    main_tkinter()