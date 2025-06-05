from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)
DATA_DIR = "data"

@app.route("/talk", methods=["POST"])
def talk():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"message": "⚠️ Message vide."})

        # Écrit dans message.txt
        with open(os.path.join(DATA_DIR, "message.txt"), "w") as f:
            f.write(message)

        # Attend que SEIA réponde
        for _ in range(10):  # 10 x 0.5s = 5s
            time.sleep(0.5)
            if os.path.exists(os.path.join(DATA_DIR, "reponse.txt")):
                with open(os.path.join(DATA_DIR, "reponse.txt"), "r") as f:
                    reponse = f.read()
                    if reponse.strip() != "":
                        return jsonify({"message": reponse})

        return jsonify({"message": "⏳ SEIA n'a pas encore répondu."})
    except Exception as e:
        return jsonify({"message": f"❌ Erreur serveur Flask : {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
