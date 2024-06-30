from flask import Flask, request

app = Flask(__name__)

@app.route("/response", methods = ["POST"])
def get_form_response():
    body = request.get_json()
    question = body["Ask your question"]
    documents = body["Upload your documents"]
    return { "success": True }

app.run()
