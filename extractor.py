from flask import Flask, render_template, request
from openai import OpenAI
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/post_url', methods=['POST'])
def post_url():
    name = "Name: not found"
    research = "Research: not found"
    email = "Email: not found"
    try:
        url = requests.get(request.form['url'])
        if url.status_code == 200:
            allTaggedContent = BeautifulSoup(url.content, 'html.parser')
            allContent = allTaggedContent.get_text()
            chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens = 250,
            messages=[
                    {"role": "user", "content": f"From the following content, please extract the following information:\n1. Name of the individual\n2. Field of research (with basic details)\n3. Email address\n\nContent:\n{allContent}\n\nUse the format:\nName: ...\nField of Research: ...\nEmail Address: ..."}
                ]
            )
            gptResponse = chat_completion.choices[0].message.content
            lines = gptResponse.split('\n')
            tempName = lines[0].split("Name: ")[1].strip()
            tempResearch = lines[1].split("Field of Research: ")[1].strip()
            tempEmail = lines[2].split("Email Address: ")[1].strip()
            name = "Name: " + tempName
            research = "Research: " + tempResearch
            email = "Email: " + tempEmail
    finally:   
        return render_template("index.html", name=name, research=research, email=email)


if __name__ == '__main__':
    app.run(debug=True)
