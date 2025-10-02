import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from components import GestionnaireTaches, Tache

gestionnaire = GestionnaireTaches()


def update_task_treeview(tree: ttk.Treeview):
    """Efface et met à jour le treeview avec les tâches du gestionnaire."""
    # Configurer les tags de couleur (peut être appelé plusieurs fois sans problème)
    tree.tag_configure('terminé', foreground='green')
    tree.tag_configure('en_cours', foreground='red')

    # Vider l'arbre
    for item in tree.get_children():
        tree.delete(item)

    # Ajouter les nouvelles tâches
    for i, tache in enumerate(gestionnaire.taches):
        if tache.etat:
            etat_texte = "Terminé"
            tag_a_appliquer = 'terminé'
        else:
            etat_texte = "En cours"
            tag_a_appliquer = 'en_cours'

        tree.insert("", tk.END, iid=i, values=(etat_texte, tache.nom), tags=(tag_a_appliquer,))


def toggle_task_state(event):
    """Gère le double-clic sur une tâche pour basculer son état."""
    tree = event.widget
    selection = tree.selection()

    if not selection:
        return  # Si aucun élément n'est sélectionné

    item_iid = selection[0]
    # L'iid de l'item correspond à son index dans la liste de tâches
    try:
        selected_index = int(item_iid)
        task = gestionnaire.taches[selected_index]
        task.basculer_etat()

        # Rafraîchir l'affichage pour montrer le changement
        update_task_treeview(tree)
    except (ValueError, IndexError):
        # Au cas où l'iid ne serait pas un index valide
        pass


def load_file_W(tree: ttk.Treeview):
    """Ouvre un explorateur de fichiers pour charger un fichier JSON,
    met à jour le gestionnaire de tâches et rafraîchit le treeview."""
    filepath = filedialog.askopenfilename(
        title="Choisir un fichier",
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
    )
    if not filepath:
        return  # L'utilisateur a annulé

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            gestionnaire.taches = [Tache.from_dict(d) for d in data]
            update_task_treeview(tree)
            messagebox.showinfo("Succès", f"{len(gestionnaire.taches)} tâches chargées.")
        else:
            messagebox.showerror("Erreur de format", "Le fichier JSON n'est pas valide.")

    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier n'a pas été trouvé.")
    except json.JSONDecodeError:
        messagebox.showerror("Erreur", "Le fichier n'est pas un JSON valide.")
    except Exception as e:
        messagebox.showerror("Erreur inattendue", f"Une erreur est survenue: {e}")


def add_task_from_gui(entry: tk.Entry, tree: ttk.Treeview):
    """Ajoute une tâche à partir du champ de saisie de l'IHM."""
    task_name = entry.get().strip()
    if not task_name:
        messagebox.showwarning("Champ vide", "Veuillez entrer un nom pour la tâche.")
        return

    gestionnaire.ajouter_tache(task_name)
    entry.delete(0, tk.END)
    update_task_treeview(tree)


def remove_task_from_gui(tree: ttk.Treeview):
    """Supprime la tâche sélectionnée dans l'IHM."""
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une tâche à supprimer.")
        return

    item_iid = selection[0]
    try:
        selected_index = int(item_iid)
        task_name = gestionnaire.taches[selected_index].nom
        if messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer la tâche \"{task_name}\" ?"):
            gestionnaire.supprimer_tache(selected_index + 1)
            update_task_treeview(tree)
    except (ValueError, IndexError):
        messagebox.showerror("Erreur", "Impossible de supprimer la tâche sélectionnée.")


def toggle_state_from_gui(tree: ttk.Treeview):
    """Bascule l'état de la tâche sélectionnée."""
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une tâche à modifier.")
        return

    item_iid = selection[0]
    try:
        selected_index = int(item_iid)
        gestionnaire.basculer_etat(selected_index + 1)
        update_task_treeview(tree)
    except (ValueError, IndexError):
        messagebox.showerror("Erreur", "Impossible de modifier la tâche sélectionnée.")

def save_file_W():
    """Ouvre un explorateur de fichiers pour sauvegarder les tâches dans un fichier JSON."""
    filepath = filedialog.asksaveasfilename(
        title="Sauvegarder les tâches",
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
        defaultextension=".json"
    )
    if not filepath:
        return  # L'utilisateur a annulé

    try:
        gestionnaire.sauvegarder(filepath)
        messagebox.showinfo("Succès", f"Tâches sauvegardées dans {filepath}")
    except Exception as e:
        messagebox.showerror("Erreur inattendue", f"Une erreur est survenue lors de la sauvegarde: {e}")