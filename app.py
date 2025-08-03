from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Set your OpenAI API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def home():
    return "Your AI Email Web App is running!"

@app.route('/summarise', methods=['POST'])
def summarise_email():
    data = request.get_json()
    email_content = data.get('email', '')

    if not email_content:
        return jsonify({'error': 'Email content is required'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Summarise this email in clear and simple terms."},
                {"role": "user", "content": email_content}
            ],
            temperature=0.5
        )

        summary = response.choices[0].message.content.strip()
        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
