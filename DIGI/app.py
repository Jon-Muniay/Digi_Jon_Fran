from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv(dotenv_path='./DIGI/api.nv')  # Ajusta si tu archivo .env está aquí

# Obtener la API Key de Hugging Face
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Nombre del modelo gratuito
model_url = "https://api-inference.huggingface.co/models/google/flan-t5-small"

# Configurar headers
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    payload = {
        "inputs": f"Analyse if it is true or false satating your reasons IN SPANISH: {user_message}. YOU ARE A SPANISH SPEAKER. ANSWER IN SPANISH.",
        # Las respuestas son muy malas, pero no he encontrado otro modelo gratuito mejor con el que probar.
    }

    try:
        response = requests.post(model_url, headers=headers, json=payload)
        response.raise_for_status()  # Esto lanza error si no es 200

        result = response.json()
        bot_message = result[0]['generated_text']

        return jsonify({'response': bot_message})

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión a Hugging Face: {e}")
        return jsonify({'error': 'Error de conexión a Hugging Face'}), 500

    except Exception as e:
        print(f"Error general: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
