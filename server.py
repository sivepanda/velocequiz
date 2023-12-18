import json
import os
import pdfplumber
import logging
import math
from dotenv import load_dotenv
from flask import Flask, request, flash, redirect, url_for
from flask_cors import CORS
from openai import OpenAI

from sklearn.cluster import KMeans
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.openai_functions import (
    create_structured_output_runnable,
)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_APIKEY"))

app = Flask(__name__)

CORS(app)

# Define the structure of the prompt
prompt_structure = """
Read the following text and generate {number} multiple choice questions based on its content. For each question, provide four options (A, B, C, D), only one of which is correct.

Text: 
{text}

Questions:
"""

# Create an instance of the PromptTemplate class
mcq_template = PromptTemplate(
    template=prompt_structure,
    input_variables=["text", "number"],
)

# Defines the JSON Schema to be used to format the answers
json_schema = {
    "title": "Question",
    "description": "Identifying information about a question.",
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

# Returns text completions from OpenAI
def get_completion(prompt, model="gpt-4"):
    """returns text completions from OpenAI"""
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        stream=False,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content


# Returns embeddings from OpenAI
def get_embedding(text, model="text-embedding-ada-002"):
    """returns embeddings from OpenAI"""
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

# Ensures the output is in a standard JSON format readable by the frontend
def get_structured_response(prompt, number=1, model="gpt-3.5-turbo"):
    """Ensures the output is in a standard JSON format readable by the frontend"""
    print("Generating a JSON Response...")

    numbered_json_schema = {
        "title": "GenQuestionContainer",
        "type": "object",
        "properties": {
            "question": {
                "title": "GeneratedQuestions",
                "type": "array",
                "description": "list of elements",
                "items": json_schema
            }
        },
        "required": ["question"],
    }

    openai_lc = ChatOpenAI(api_key=os.getenv("OPENAI_APIKEY"), model=model, temperature=0)
    runnable = create_structured_output_runnable(output_schema=numbered_json_schema, llm=openai_lc, prompt=mcq_template)
    return runnable.invoke({"text": str(prompt), "number": int(number)})

# Read PDF from path and return the text of each page as a list of strings
def read_pdf(pdf_path):
    """Read PDF from path and return the text of each page as a list of strings"""
    print("Opening PDF...")
    with pdfplumber.open(pdf_path) as pdf:
        text = []
        for page in pdf.pages:
            text.append(page.extract_text())
    return text


def get_topics(pdf_path):
    print("Reading text...")
    list_pdf_text = read_pdf(pdf_path)
    full_text = []
    for page_text in list_pdf_text:
        if(len(page_text) > 10):
            full_text.append(page_text.replace("\n", " -- "))

    print("Generating embeddings...")
    embeddings = [get_embedding(segment) for segment in full_text]

    print("Grouping clusters...")
    # Use K-means clustering
    # 1/3 length of total embeddings if num embeddings > 5 else 3
    n_clusters = math.floor(len(embeddings) / 3) if len(embeddings) > 5 else 3
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(embeddings)
    labels = kmeans.labels_

    print("Sorting text...")
    # Group text segments by their cluster labels
    topics = {}
    for i, label in enumerate(labels):
        if label not in topics:
            topics[label] = []
        topics[label].append(full_text[i])

    print("Generating text topic names...")
    # convert number labels to readable text and return a dict
    topic_groups = []
    for topic in topics:
        topic_obj = {}
        text = ''
        for text_segment in topics[topic]:
            text += text_segment
        topic_name = get_completion("What is the common topic in this text in 3 words or less?" + text)
        topic_obj["name"] = topic_name
        topic_obj['text'] = text
        topic_groups.append(topic_obj)
    return json.dumps(topic_groups)


# Use an input path to a PDF or filestream, reads each page of the PDF and returns either a question or a string containing "null"
def get_pdf_qa(pdf_path):
    """Use an input path to a PDF or filestream, reads each page of the PDF and returns either a question or a string containing 'null'"""
    output = []
    list_pdf_text = read_pdf(pdf_path)

    for page_text in list_pdf_text:
        
        # filter out pages that do not have enough text for an adequate response 
        if(len(page_text) > 100):
            response = get_structured_response(page_text)

            # comment above and uncomment below to use the dummy response that does not contact OpenAI servers
            # response = '{"question": {"content": "What could be the possible intentions of a nation-state hacker?","responses": [{"content": "A. To disclose or disrupt", "correct": true},{"content": "B. To entertain or educate", "correct": false},{"content": "C. To create or innovate", "correct": false},{"content": "D. To support or assist", "correct": false}]}}'
            
            for q in response['question']:
                output.append(q)
    
    return output


# Use an input JSON, reads each text chunk and returns specified number of questions string containing 'null'
def get_json_qa(json_obj):
    """Use an input JSON, reads each text chunk and returns specified number of questions string containing 'null'"""
    output = []
    for text in json_obj:
        words = text['text']
        # filter out pages that do not have enough text for an adequate response 
        if(len(text['text']) > 100  and (int(text['numQuestions']) != 0)):
            response = get_structured_response(words, number=text['numQuestions'])
            
            for q in response['question']:
                output.append(q)

    return output


ALLOWED_EXTENSIONS = {"txt", "pdf", "md"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 megabytes

@app.route("/quiz", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        print("/quiz : Post")
        # check if the post request has the file part
        if request.files["file"] == None:
            print("no file")
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "" or not (allowed_file(file.filename)):
            print("nothing selected")
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            return get_pdf_qa(file.stream)
        else:
            return "success"
    else:
        return redirect(request.url)

@app.route("/topics", methods=["GET", "POST"])
def up_file():
    if request.method == "POST":
        print("/topics : Post")
        # check if the post request has the file part
        if request.files["file"] == None:
            print("no file")
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "" or not (allowed_file(file.filename)):
            print("nothing selected")
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            return get_topics(file.stream)
        else:
            return "success"
    else:
        return redirect(request.url)

@app.route("/topic_quiz", methods=["GET", "POST"])
def up_topics():
    if request.method == "POST":
        print("/topic_quiz : Post")
        # check if the post request has the file part
        if request.is_json == False:
            return redirect(request.url)

        return get_json_qa(request.get_json())
        
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
