import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from components import GestionnaireTaches, Tache

gestionnaire = GestionnaireTaches()

# Variables pour gérer l'infobulle
fenetre_infobulle = None
id_delai_infobulle = None

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
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")])
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
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.* ")],
        defaultextension=".json")
    if not filepath:
        return

    try:
        gestionnaire.sauvegarder(filepath)
        messagebox.showinfo("Succès", f"Tâches sauvegardées dans {filepath}")
    except Exception as e:
        messagebox.showerror("Erreur inattendue", f"Une erreur est survenue: {e}")

def afficher_infobulle(tree, text):
    """Crée et affiche la fenêtre de l'infobulle."""
    global fenetre_infobulle
    if fenetre_infobulle:
        fenetre_infobulle.destroy()

    x = tree.winfo_pointerx() + 15
    y = tree.winfo_pointery() + 10

    fenetre_infobulle = tw = tk.Toplevel(tree)
    tw.wm_overrideredirect(True)
    tw.wm_geometry(f"+{x}+{y}")
    
    label = tk.Label(tw, text=text, justify=tk.LEFT,
                     background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                     font=("tahoma", "8", "normal"))
    label.pack(ipadx=1)

def masquer_infobulle():
    """Détruit la fenêtre de l'infobulle si elle existe."""
    global fenetre_infobulle
    if fenetre_infobulle:
        fenetre_infobulle.destroy()
        fenetre_infobulle = None

def gerer_mouvement_tree(event):
    """Gère le mouvement de la souris sur le Treeview pour afficher une infobulle."""
    global id_delai_infobulle
    tree = event.widget

    if id_delai_infobulle:
        tree.after_cancel(id_delai_infobulle)
        id_delai_infobulle = None
    masquer_infobulle()

    row_id = tree.identify_row(event.y)
    column_id = tree.identify_column(event.x)

    if column_id == "#2" and row_id:
        try:
            index = int(row_id)
            task_name = gestionnaire.taches[index].nom
            id_delai_infobulle = tree.after(500, lambda: afficher_infobulle(tree, task_name))
        except (ValueError, IndexError):
            pass

def gerer_sortie_tree(event):
    """Gère la sortie de la souris du Treeview pour masquer l'infobulle."""
    global id_delai_infobulle
    tree = event.widget
    if id_delai_infobulle:
        tree.after_cancel(id_delai_infobulle)
        id_delai_infobulle = None
    masquer_infobulle()