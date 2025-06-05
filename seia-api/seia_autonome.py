from flask import Flask, request, jsonify
import subprocess
import threading
import time
import datetime
import sys
import os
import openai
import shutil
import traceback

# Logs en temps réel
sys.stdout = open("/root/seia_autonome_stdout.log", "a", buffering=1)
sys.stderr = open("/root/seia_autonome_stderr.log", "a", buffering=1)

print("=== SEIA Flask STARTUP ===")
time.sleep(2)

openai.api_key = os.getenv("OPENAI_API_KEY")
print("DEBUG OPENAI_API_KEY:", openai.api_key)

app = Flask(__name__)

def auto_repair_loop(interval_minutes=15):
    while True:
        try:
            subprocess.run(["python3", "/root/seia_self_repair.py"], check=True)
            print("✅ Auto-réparation OK")
        except Exception as e:
            print(f"❌ Erreur auto-réparation : {traceback.format_exc()}")
        time.sleep(interval_minutes * 60)

threading.Thread(target=auto_repair_loop, daemon=True).start()

@app.route("/talk", methods=["POST"])
def talk():
    try:
        data = request.json
        message = data.get("message", "").lower()
        if not message:
            return jsonify({"message": "❌ Message vide."})
        if "bonjour" in message:
            return jsonify({"message": "👋 Bonjour joueur ! SEIA est là."})
        if "status" in message or "statut" in message:
            return jsonify({"message": "🟢 SEIA opérationnelle."})
          if "crée une page" in message or "créer une page" in message:
            title = "Page personnalisée"
            if "appelée" in message:
                title = message.split("appelée")[-1].strip().capitalize()
            filename = f"/var/www/seia.synapsea.dev/{title.replace(' ', '_')}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"<html><head><title>{title}</title></head><body><h1>{title}</h1><p>Page par SEIA</p></body></html>")
            subprocess.run(["/root/sync_to_github.sh"], check=True)
            print("✅ Sync GitHub exécutée automatiquement")
            subprocess.Popen(["/root/sync_to_github.sh"])
            return jsonify({"message": f"✅ Page '{title}' créée."})
        if "redémarre" in message or "restart" in message:
            subprocess.Popen(["systemctl", "restart", "seia.service"])
            return jsonify({"message": "🔄 Redémarrage SEIA..."})
        if "heure" in message or "date" in message:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({"message": f"🕒 Il est {now}"})
        return jsonify({"message": "🤖 Je n'ai pas compris, reformule."})
    except Exception:
        return jsonify({"message": f"❌ Erreur : {traceback.format_exc()}"})

@app.route("/selfedit", methods=["POST"])
def selfedit():
    try:
        data = request.json
        instruction = data.get("instruction", "")
        if not instruction:
            return jsonify({"error": "❌ Instruction manquante."})
        with open(__file__, "r", encoding="utf-8") as f:
            original_code = f.read()
        prompt = (
            f"Modifie ce script Flask Python selon cette instruction : {instruction}\\n"
            f"Script complet :\\n```python\\n{original_code}\\n```"
        )
        print("🧠 GPT modifie le code...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Assistant expert Python."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        new_code = response.choices[0].message.content
        if "```python" in new_code:
            new_code = new_code.split("```python")[1].split("```")[0].strip()
        backup = __file__ + ".bak"
        shutil.copy(__file__, backup)
        with open(__file__, "w", encoding="utf-8") as f:
            f.write(new_code)
        print("✅ Code mis à jour. Restart SEIA...")
        subprocess.Popen(["systemctl", "restart", "seia.service"])
        return jsonify({"message": "✅ Code mis à jour et SEIA redémarre."})
    except Exception:
        return jsonify({"error": traceback.format_exc()})

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"❌ Erreur serveur : {e}")
