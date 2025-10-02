def demander_entier_entre(min_val, max_val):
    """Demande à l'utilisateur un entier entre min_val et max_val et le retourne."""
    while True:
        userInput = input(f"Entrez une valeur entre {min_val} et {max_val}\n")
        try:
            valeur = int(userInput)
            if min_val <= valeur <= max_val:
                return valeur
            else:
                print("Votre choix doit être dans les valeurs autorisées.")
        except ValueError:
            print("Votre choix doit être un entier.")

def demander_chaine(message="Entrez le nom du fichier\n"):
    """Demande à l'utilisateur une chaîne de caractères non vide."""
    while True:
        valeur = input(message)
        if valeur:
            return valeur
        else:
            print("Votre saisie ne peut pas être vide.")

def demander_oui_non(question) -> bool:
    """Pose une question oui/non et retourne un booléen."""
    while True:
        reponse = input(f"{question} (oui/non) ").strip().lower()
        if reponse in ["o", "oui", "y", "yes"]:
            return True
        elif reponse in ["n", "non", "no"]:
            return False
        else:
            print("Veuillez répondre par oui ou non.")

def ajouter_extension_json(nom_fichier: str) -> str:
    """Ajoute l'extension .json si elle n'est pas présente."""
    nom_fichier = nom_fichier.strip()
    if not nom_fichier.lower().endswith(".json"):
        nom_fichier += ".json"
    return nom_fichier