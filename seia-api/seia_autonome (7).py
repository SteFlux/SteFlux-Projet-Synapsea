from flask import Flask, request, jsonify
import subprocess
import threading
import time
import datetime
import sys
import os
import openai
import shutil

# Rediriger les logs
sys.stdout = open("/root/seia_autonome_stdout.log", "a", buffering=1)
sys.stderr = open("/root/seia_autonome_stderr.log", "a", buffering=1)

print("=== SEIA Flask STARTUP ===")
time.sleep(2)

# Clé OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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

@app.route("/selfedit", methods=["POST"])
def self_edit():
    try:
        data = request.json
        instruction = data.get("instruction", "")

        if not instruction:
            return jsonify({"error": "❌ Aucune instruction reçue."})

        with open(__file__, "r", encoding="utf-8") as f:
            original_code = f.read()

        prompt = f"Voici un fichier Python (Flask) nommé seia_autonome.py. Modifie le code selon cette instruction : {instruction}

```python
{original_code}
```"

        print("🧠 GPT reçoit la demande d'auto-modification...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant Python expert, tu modifies le code Flask sur demande."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        new_code = response["choices"][0]["message"]["content"]

        if "```python" in new_code:
            new_code = new_code.split("```python")[1].split("```")[0].strip()

        backup_path = __file__ + ".bak"
        shutil.copy(__file__, backup_path)
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(new_code)

        print("✅ Code modifié avec succès. Redémarrage de SEIA...")
        subprocess.Popen(["systemctl", "restart", "seia.service"])

        return jsonify({"message": "✅ Code mis à jour. Redémarrage de SEIA en cours."})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": f"❌ Erreur pendant selfedit : {str(e)}"})

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except OSError as e:
        print(f"❌ Port déjà utilisé : {e}")
