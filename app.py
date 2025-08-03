from flask import Flask, request, render_template_string
import openai
import os

# Load the API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Email Tool</title>
</head>
<body>
    <h1>Email Summariser and Reply Assistant</h1>
    <form method="post">
        <textarea name="email" rows="15" cols="80" placeholder="Paste your email here...">{{ request.form.email }}</textarea><br><br>
        <input type="submit" value="Summarise and Draft Reply">
    </form>
    {% if summary %}
        <h2>Summary:</h2>
        <p>{{ summary }}</p>
    {% endif %}
    {% if reply %}
        <h2>Suggested Reply:</h2>
        <p>{{ reply }}</p>
    {% endif %}
</body>
</html>
"""

def summarise_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Summarise emails clearly in bullet points for someone short on time."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    return response['choices'][0]['message']['content'].strip()

def draft_reply(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Write a brief, professional email reply in a polite tone."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.3
    )
    return response['choices'][0]['message']['content'].strip()

@app.route("/", methods=["GET", "POST"])
def home():
    summary = None
    reply = None
    if request.method == "POST":
        email_text = request.form["email"]
        summary = summarise_text(email_text)
        reply = draft_reply(email_text)
    return render_template_string(HTML_TEMPLATE, summary=summary, reply=reply)

if __name__ == "__main__":
    app.run(debug=True)
