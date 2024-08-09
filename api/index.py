from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialiser l'application Flask
app = Flask(__name__)

# Configurer l'API Google Generative AI avec la clé API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configurer le modèle avec les paramètres de génération
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
)

# Définir une route pour gérer les requêtes GET et POST à '/chat'
@app.route('/chat', methods=['GET', 'POST'])
def generate_response():
    if request.method == 'GET':
        # Récupérer les paramètres de l'URL pour les requêtes GET
        prompt = request.args.get("prompt", "")
        style = request.args.get("style", "")
        context = request.args.get("context", "")
    else:
        # Récupérer le corps de la requête JSON pour les requêtes POST
        data = request.get_json()
        prompt = data.get("prompt", "")
        style = data.get("style", "")
        context = data.get("context", "")

    # Vérifier si le prompt est vide
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Modifier dynamiquement le prompt en fonction des paramètres
    if context:
        prompt = f"Contexte: {context}\n\n{prompt}"
    if style:
        prompt = f"{prompt}\n\nVeuillez répondre dans un style {style}."

    # Commencer une session de chat avec le prompt modifié
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [prompt]}
        ]
    )

    # Envoyer le message et obtenir la réponse du modèle
    response = chat_session.send_message(prompt)

    # Retourner la réponse sous forme de JSON
    return jsonify({"response": response.text})

# Exécuter l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
