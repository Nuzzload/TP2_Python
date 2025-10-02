import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from components import GestionnaireTaches, Tache

gestionnaire = GestionnaireTaches()

def mettre_a_jour_liste_taches(tree: ttk.Treeview):
    """Efface et met à jour l'arbre avec les tâches du gestionnaire."""
    # Configuration des tags pour les couleurs
    tree.tag_configure('terminé', foreground='green')
    tree.tag_configure('en_cours', foreground='red')
    tree.tag_configure('oddrow', background='white')
    tree.tag_configure('evenrow', background='#E8E8E8')

    # Vider l'arbre
    for item in tree.get_children():
        tree.delete(item)

    # Ajouter les tâches
    for i, tache in enumerate(gestionnaire.taches):
        tag_ligne = 'evenrow' if i % 2 == 0 else 'oddrow'
        
        if tache.etat:
            etat_texte = "Terminé"
            tag_etat = 'terminé'
        else:
            etat_texte = "En cours"
            tag_etat = 'en_cours'

        tree.insert("", tk.END, iid=i, values=(etat_texte, tache.nom), tags=(tag_ligne, tag_etat))

def basculer_etat_double_clic(event):
    """Gère le double-clic sur une tâche pour basculer son état."""
    tree = event.widget
    selection = tree.selection()

    if not selection:
        return

    item_id = selection[0]
    try:
        index_selection = int(item_id)
        tache = gestionnaire.taches[index_selection]
        tache.basculer_etat()
        mettre_a_jour_liste_taches(tree)
    except (ValueError, IndexError):
        pass

def charger_fichier(tree: ttk.Treeview):
    """Ouvre un explorateur de fichiers pour charger un fichier JSON."""
    filepath = filedialog.askopenfilename(
        title="Choisir un fichier",
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
    )
    if not filepath:
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            gestionnaire.taches = [Tache.from_dict(d) for d in data]
            mettre_a_jour_liste_taches(tree)
            messagebox.showinfo("Succès", f"{len(gestionnaire.taches)} tâches chargées.")
        else:
            messagebox.showerror("Erreur de format", "Le fichier JSON n'est pas valide.")
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Erreur", "Impossible de lire le fichier.")
    except Exception as e:
        messagebox.showerror("Erreur inattendue", f"Une erreur est survenue: {e}")

def ajouter_tache_ihm(entry: tk.Entry, tree: ttk.Treeview):
    """Ajoute une tâche depuis le champ de saisie."""
    nom_tache = entry.get().strip()
    if not nom_tache:
        messagebox.showwarning("Champ vide", "Veuillez entrer un nom pour la tâche.")
        return

    gestionnaire.ajouter_tache(nom_tache)
    entry.delete(0, tk.END)
    mettre_a_jour_liste_taches(tree)

def supprimer_tache_ihm(tree: ttk.Treeview):
    """Supprime la tâche sélectionnée."""
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une tâche.")
        return

    item_id = selection[0]
    try:
        index_selection = int(item_id)
        nom_tache = gestionnaire.taches[index_selection].nom
        if messagebox.askyesno("Confirmation", f"Supprimer la tâche \"{nom_tache}\" ?"):
            gestionnaire.supprimer_tache(index_selection + 1)
            mettre_a_jour_liste_taches(tree)
    except (ValueError, IndexError):
        messagebox.showerror("Erreur", "Impossible de supprimer la tâche.")

def basculer_etat_ihm(tree: ttk.Treeview):
    """Bascule l'état de la tâche sélectionnée."""
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une tâche.")
        return

    item_id = selection[0]
    try:
        index_selection = int(item_id)
        gestionnaire.basculer_etat(index_selection + 1)
        mettre_a_jour_liste_taches(tree)
    except (ValueError, IndexError):
        messagebox.showerror("Erreur", "Impossible de modifier la tâche.")

def sauvegarder_fichier():
    """Ouvre un explorateur de fichiers pour sauvegarder les tâches."""
    filepath = filedialog.asksaveasfilename(
        title="Sauvegarder les tâches",
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")],
        defaultextension=".json"
    )
    if not filepath:
        return

    try:
        gestionnaire.sauvegarder(filepath)
        messagebox.showinfo("Succès", f"Tâches sauvegardées dans {filepath}")
    except Exception as e:
        messagebox.showerror("Erreur inattendue", f"Une erreur est survenue: {e}")
