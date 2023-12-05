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
from openai.embeddings_utils import get_embedding
from langchain.chains.openai_functions import (
    create_structured_output_runnable,
)

from sklearn.cluster import KMeans

load_dotenv()

openai.api_key = os.getenv("OPENAI_APIKEY")

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

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model).data[0].embedding

# use an input path to a PDF or filestream, reads each page of the PDF and returns either a question or a string containing "null"
def get_topics(pdf_path):
    output = []
    list_pdf_text = read_pdf(pdf_path)

    full_text = []

    for page_text in list_pdf_text:
        full_text.append(page_text.replace("\n", " -- "))
    
    return full_text

def get_completion(prompt, model="gpt-4"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

text_segments = get_topics('./CIATR.pdf')

# Generate embeddings
embeddings = [get_embedding(segment) for segment in text_segments]

# Use K-means clustering
n_clusters = 5  # Example number of clusters
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(embeddings)
labels = kmeans.labels_

# Group text segments by their cluster labels
topics = {}
for i, label in enumerate(labels):
    if label not in topics:
        topics[label] = []
        print('l',label)
    topics[label].append(text_segments[i])

for topic in topics:
    text = ''
    for text_segment in topics[topic]:
        text += text_segment
    print(get_completion("What is the common topic in this text in 3 words or less?" + text))

