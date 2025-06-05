import time
from modules.comprehension import analyser
from modules.action import executer
from modules.memoire import charger_etat, sauvegarder_etat

etat = charger_etat()

def boucle_agent():
    while True:
        try:
            with open("data/message.txt", "r") as f:
                message = f.read().strip()

            if message:
                print(f"[SEIA] Message reçu : {message}")
                intention = analyser(message)
                reponse, nouvel_etat = executer(intention, etat)
                sauvegarder_etat(nouvel_etat)

                with open("data/reponse.txt", "w") as f:
                    f.write(reponse)
                with open("data/message.txt", "w") as f:
                    f.write("")

                print(f"[SEIA] Réponse envoyée : {reponse}")
        except Exception as e:
            print(f"[SEIA] Erreur : {e}")

        time.sleep(1)

if __name__ == "__main__":
    boucle_agent()
