from flask import Flask, jsonify, request
import json, os

app = Flask(__name__)

# fix path nonsense

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


# codehint api

from cobert import codehint


@app.route("/codehint", methods=["POST"])
def apicodehint():
    code = request.json.get("code")
    result = codehint(code)
    return jsonify(result)


# codesyntax api

from codesyntax import codesyntax


@app.route("/codesyntax", methods=["POST"])
def apicodesyntax():
    code = request.json.get("code")
    result = codesyntax(code[:512])
    return jsonify({"lang": result})


# codegenerator api
# this consumes too much vram (4.5gb~)

from replit_codeinstruct import codegenerator


@app.route("/codegenerator", methods=["POST"])
def apicodegenerator():
    prompt = request.json.get("prompt")
    context = request.json.get("context")
    result = codegenerator(prompt, context)
    return jsonify({"output": result})


# server start
app.run(debug=False, port=4654)
