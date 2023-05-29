from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# codehint api

from cobert import codehint


@app.route("/codehint", methods=["POST"])
def apicodehint():
    code = request.json.get("code")
    result = codehint(code)
    return jsonify(result)


# codesyntax hint api

from codesyntax import codesyntax


@app.route("/codesyntax", methods=["POST"])
def apicodesyntax():
    code = request.json.get("code")
    result = codesyntax(code[:512])
    return jsonify({"lang": result})


# server start
app.run(debug=False, port=4654)
