

def checkIntBetweenXandY(X, Y):
    while 1:
        userInput = input("Entrez une valeur entre " + str(X) + " et " + str(Y) + "\n")
        try:
            value=int(userInput)
            if X <= value <= Y:
                return value
            else:
                print("Votre choix doit rentrer dans les valeurs autorisées")
        except ValueError:
            print("Votre choix doit être un entier")

def checkString():
    while 1:
        value = input("Entrez le nom du fichier\n")
        if value == "":
            print("Votre nom de fichier doit contenir au moins 1 caractère.")
        else:
            return value

def checkOuiOuNon(question) -> bool:
    while 1:
        reponse = input(question + "Oui ou non ?").strip().lower()
        if reponse in ["o", "oui", "y", "yes"]:
            return True
        elif reponse in ["n", "non", "no"]:
            return False
        else:
            print("Veuillez rentrer une réponse valide.")


def checkExtensionJson(fname: str) -> str:
    fname = fname.strip()
    if not fname.lower().endswith(".json"):
        fname += ".json"
    return fname


