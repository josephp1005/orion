from flask import Flask, request, jsonify
from flask_cors import CORS
from answer import docs_and_response

app = Flask(__name__)
CORS(app)

@app.route("/output")
def output():
    query = request.args.get('query')
    try:
        response = docs_and_response(query)
        return response
    except:
        return "AI service is not running."

if __name__ == '__main__':
    app.run(port=5050)