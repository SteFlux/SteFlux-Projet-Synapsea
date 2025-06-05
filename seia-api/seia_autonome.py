from flask import Flask, request, jsonify
import subprocess
import threading
import time
import datetime
import sys
sys.stdout = open("/root/seia_autonome_stdout.log", "a", buffering=1)
sys.stderr = open("/root/seia_autonome_stderr.log", "a", buffering=1)


print("=== SEIA Flask STARTUP ===")
time.sleep(5)

app = Flask(__name__)

# --- Démarrage du thread d'auto-réparation toutes les 15 minutes ---
def auto_repair_loop(interval_minutes=15):
    while True:
        try:
            subprocess.run(["python3", "/root/seia_self_repair.py"], check=True)
            print("✅ Auto-réparation exécutée")
        except Exception as e:
            print(f"❌ Erreur auto-réparation : {e}")
        time.sleep(interval_minutes * 60)

repair_thread = threading.Thread(target=auto_repair_loop, daemon=True)
repair_thread.start()

@app.route("/talk", methods=["POST"])
def talk():
    data = request.json
    message = data.get("message", "").lower()

    if not message:
        return jsonify({"message": "❌ Je n'ai pas reçu de message."})

    if "bonjour" in message:
        return jsonify({"message": "👋 Bonjour joueur ! Je suis SEIA, ton assistante IA sur Synapsea."})

    if "status" in message or "statut" in message:
        return jsonify({"message": "🟢 SEIA fonctionne correctement et est connectée."})

    if "crée une page" in message or "créer une page" in message:
        try:
            title = "Page personnalisée"
            if "appelée" in message:
                title = message.split("appelée")[-1].strip().capitalize()
            filename = f"/var/www/seia.synapsea.dev/{title.replace(' ', '_')}.html"
            print(f"DEBUG: tentative de création du fichier {filename}")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"<html><head><title>{title}</title></head><body><h1>{title}</h1><p>Page générée par SEIA</p></body></html>")
            print(f"DEBUG: fichier créé avec succès")
            return jsonify({"message": f"✅ Page HTML '{title}' créée avec succès."})
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Erreur création page: {error_details}")
            return jsonify({"message": f"❌ Erreur lors de la création de la page : {str(e)}"})

    if "redémarre" in message or "restart" in message:
        subprocess.Popen(["systemctl", "restart", "seia.service"])
        return jsonify({"message": "🔄 SEIA est en cours de redémarrage..."})

    if "heure" in message or "date" in message:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return jsonify({"message": f"🕒 Il est {now}."})

    return jsonify({"message": "🤖 SEIA n’a pas compris ta demande. Essaie de reformuler."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
