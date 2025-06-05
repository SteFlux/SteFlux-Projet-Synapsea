import json
import os

def charger_etat():
    if os.path.exists("data/etat.json"):
        try:
            with open("data/etat.json", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def sauvegarder_etat(etat):
    with open("data/etat.json", "w") as f:
        json.dump(etat, f)
