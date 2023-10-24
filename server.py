import json
import openai
import os
import pdfplumber
import logging
from dotenv import load_dotenv
from flask import Flask, request, flash, redirect, url_for
from flask_cors import CORS

load_dotenv()

openai.api_key = os.getenv("OPENAI_APIKEY")

app = Flask(__name__)

CORS(app)


# Read PDF from path and return the text of each page as a list of strings
def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = []
        for page in pdf.pages:
            text.append(page.extract_text())
    return text


# Returns a response to the inputted prompt
def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# use an input path to a PDF or filestream, reads each page of the PDF and returns either a question or a string containing "null"
def get_qa(pdf_path):
    output = []
    list_pdf_text = read_pdf(pdf_path)

    for page_text in list_pdf_text:
        prompt = f"""
        Generate one multi-choice question and its answers for the following text. Each question has 
        *four* lettered choices and there is only *one* correct answer.  Return the question as JSON.
        \nA sample response would look like this:\n\n {{ question: {{
        \"content\": \"What is 2+2?\",
        \"responses\": \[\{{\"content\: A. 4, \"correct": true\}}, \{{\"content\": B. 7\}}\, \{{\"content\": C. 1\}}\,
        \{{\"content\": D. 22\}}\]\n}}\n}}\n\nWhile questions must be based on the text, 
        questions must be able to be answered without direct  access to the text - quiz 
        on understanding concepts. Questions cannot have a basis on what information  is or 
        is not included in the text; only on the concepts covered in the text. If there is not 
        enough information to generate a question, do not generate a question. Instead, reply with "null" \
        ```{page_text}```
        """

        # response = get_completion(prompt)
        response = '{"question": {"content": "What could be the possible intentions of a nation-state hacker?","responses": [{"content": "To diisclose or disrupt", "correct": true},{"content": "To entertain or educate", "correct": false},{"content": "To create or innovate", "correct": false},{"content": "To support or assist", "correct": false}]}}'
        output.append(response)
        print("\n\n\n", response)

    return output


ALLOWED_EXTENSIONS = {"txt", "pdf", "md"}


# @app.route('/upload', methods=['GET', 'POST'])
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        print("Post")
        # check if the post request has the file part
        if request.files["file"] == None:
            print("no file")
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        print(file)

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "" or not (allowed_file(file.filename)):
            print("nothing selected")
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            return get_qa(file.stream)
        else:
            return "success"
    else:
        return redirect(request.url)


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
        level=logging.INFO,
    )
    app.secret_key = os.getenv("APPKEY_FLASK")
    app.config["SESSION_TYPE"] = "filesystem"
    # app.config['']

    app.run(debug=True)
