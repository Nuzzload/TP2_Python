import tkinter as tk
from tkinter import ttk

from functionsTKINTER import gestionnaire, load_file_W, toggle_task_state, add_task_from_gui, remove_task_from_gui, toggle_state_from_gui, save_file_W

root = tk.Tk()
root.title("Gestionnaire de tâches")
root.geometry("600x500")
# La fenêtre est maintenant redimensionnable par défaut

# --- Widgets pour afficher la liste ---
# Frame pour la listbox et les scrollbars
list_frame = tk.Frame(root)
# Le expand=True centre le bloc dans la fenêtre. padx et pady ajoutent de l'espace autour.
list_frame.pack(pady=20, padx=20, expand=True)

# On utilise grid() à l'intérieur de list_frame pour un meilleur contrôle
list_frame.grid_rowconfigure(0, weight=1)
list_frame.grid_columnconfigure(0, weight=1)

# Treeview pour un affichage en colonnes
tree = ttk.Treeview(list_frame, columns=("state", "name"), show="headings", height=10)
tree.heading("state", text="État")
tree.heading("name", text="Tâche")
tree.column("state", width=80, anchor="center", stretch=tk.NO)
tree.column("name", width=300, stretch=tk.NO)

tree.grid(row=0, column=0, sticky="nsew")
tree.bind("<Double-1>", toggle_task_state)

# Scrollbar Verticale
y_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
y_scrollbar.grid(row=0, column=1, sticky="ns")
tree.config(yscrollcommand=y_scrollbar.set)

# Scrollbar Horizontale
x_scrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=tree.xview)
x_scrollbar.grid(row=1, column=0, sticky="ew")
tree.config(xscrollcommand=x_scrollbar.set)


# --- Widgets pour l'ajout de tâches ---
add_frame = tk.Frame(root)
add_frame.pack(pady=(0, 10), padx=20, fill="x")

task_entry = tk.Entry(add_frame)
task_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))

add_button = tk.Button(add_frame, text="Ajouter", command=lambda: add_task_from_gui(task_entry, tree))
add_button.pack(side=tk.RIGHT)


# --- Frame for action buttons ---
action_frame = tk.Frame(root)
action_frame.pack(pady=10, padx=20, fill="x")

toggle_button = tk.Button(action_frame, text="Changer État", command=lambda: toggle_state_from_gui(tree))
toggle_button.pack(side=tk.LEFT, expand=True, padx=5)

delete_button = tk.Button(action_frame, text="Supprimer", command=lambda: remove_task_from_gui(tree))
delete_button.pack(side=tk.LEFT, expand=True, padx=5)


# --- Barre de Menus ---
menubar = tk.Menu(root)

# Création d'un menu "Fichier"
menu_fichier = tk.Menu(menubar, tearoff=0)
menu_fichier.add_command(label="Sauvegarder", command=save_file_W)
menu_fichier.add_command(label="Charger", command=lambda: load_file_W(tree))
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=root.quit)

# Ajout du menu "Fichier" dans la barre
menubar.add_cascade(label="Fichier", menu=menu_fichier)

# On attache la barre de menus à la fenêtre
root.config(menu=menubar)




root.mainloop()