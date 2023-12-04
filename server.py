import json
import openai
import os
import pdfplumber
import logging
from dotenv import load_dotenv
from flask import Flask, request, flash, redirect, url_for
from flask_cors import CORS

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.openai_functions import (
    create_structured_output_runnable,
)

load_dotenv()

openai.api_key = os.getenv("OPENAI_APIKEY")

app = Flask(__name__)

CORS(app)

# Define the structure of the prompt
prompt_structure = """
Read the following text and generate one multiple choice question based on its content. For each question, provide four options (A, B, C, D), only one of which is correct.

Text: 
{text}

Questions:
"""

# Create an instance of the PromptTemplate class
mcq_template = PromptTemplate(
    template=prompt_structure,
    input_variables=["text"],
)

# Defines the JSON Schema to be used to format the answers
json_schema = {
    "title": "Person",
    "description": "Identifying information about a person.",
    "type": "object",
    "properties": {
        "content": {"title": "Content", "description": "The content of the question", "type": "string"},
        "responses": {
                "title": "Response",
                "type": "array",
                "description": "List of response options",
                "items": {
                    "title": "Items",
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "The content of the response"
                        },
                        "correct": {
                            "type": "boolean",
                            "description": "Indicates if the response is correct"
                        }
                    },
                    "required": ["content", "correct"]
                }
            }
    },
    "required": ["content", "response"],
}

# Ensures the output is in a standard JSON format readable by the frontend
def get_structured_response(prompt, model="gpt-3.5-turbo"):
    openai_lc = ChatOpenAI(api_key=os.getenv("OPENAI_APIKEY"), model=model, temperature=0)
    runnable = create_structured_output_runnable(output_schema=json_schema, llm=openai_lc, prompt=mcq_template)
    return runnable.invoke({"text": str(prompt)})

# Read PDF from path and return the text of each page as a list of strings
def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = []
        for page in pdf.pages:
            text.append(page.extract_text())
    return text


# use an input path to a PDF or filestream, reads each page of the PDF and returns either a question or a string containing "null"
def get_qa(pdf_path):
    output = []
    list_pdf_text = read_pdf(pdf_path)

    for page_text in list_pdf_text:
        
        # filter out pages that do not have enough text for an adequate response 
        if(len(page_text) > 100):
            response = get_structured_response(page_text)
            output.append('{"question":' + json.dumps(response) + "}")
            print("\n\n\n", response)

        # comment above and uncomment below to use the dummy response that does not contact OpenAI servers
        # response = '{"question": {"content": "What could be the possible intentions of a nation-state hacker?","responses": [{"content": "A. To disclose or disrupt", "correct": true},{"content": "B. To entertain or educate", "correct": false},{"content": "C. To create or innovate", "correct": false},{"content": "D. To support or assist", "correct": false}]}}'
        

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
