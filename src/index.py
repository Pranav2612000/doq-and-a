from flask import Flask, request
import drive

app = Flask(__name__)

@app.route("/response", methods = ["POST"])
def get_form_response():
    body = request.get_json()
    question = body["Ask your question"]
    documents = body["Upload your documents"]
    for documentId in documents:
        print(f"downloading {documentId}")
        drive.download_pdf(documentId)
    return { "success": True }

app.run()
