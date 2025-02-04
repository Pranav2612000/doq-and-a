from flask import Flask, request
from pathlib import Path
from shutil import rmtree
import os

import drive
import knowledge
import query
import emailer

DATA_PATH = os.environ['DATA_PATH']
CHROMA_PATH = os.environ['CHROMA_PATH']

app = Flask(__name__)

def clear_directory(name):
	for path in Path("/path/to/folder").glob("**/*"):
		if path.is_file():
			path.unlink()
		elif path.is_dir():
			rmtree(path)

@app.route("/response", methods = ["POST"])
def get_form_response():
    body = request.get_json()
    question = body["Ask your question"]
    documents = body["Upload your documents"]
    email = body["email"]

    # Delete previous documents if any exist
    clear_directory(DATA_PATH)

    for documentId in documents:
        print(f"downloading {documentId}")
        drive.download_pdf(documentId)

    knowledge.generate_knowledge()

    response = query.get_answer(question)
    if response:
        message = f"""\
        Subject: DoQ-and-A | Answers Ready

        Q: {question}
        A: {response["response"]}
        Sources: {response["sources"]}
        """
        emailer.send_email(email, message)
        print('Email Sent')

    # Delete these saved documents and db
    clear_directory(DATA_PATH)
    clear_directory(CHROMA_PATH)
    return { "success": True }

app.run()
