from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un verificador de noticias. Analiza si una noticia que te envía el usuario parece verdadera o falsa y explica tu razonamiento."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_message = response['choices'][0]['message']['content']
        return jsonify({'response': bot_message})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
