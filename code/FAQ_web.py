from flask import Flask, render_template, request, url_for, redirect, jsonify
import os
from FAQAPI import FAQAPI

app = Flask(__name__)

FAQ_BASE_EMAIL_PATH = os.getenv("FAQ_BASE_EMAIL_PATH")


@app.route('/home')
def get():
    ## try to open: http://127.0.0.1:5000/get?key=mead
    key = request.args.get("key")
    print("key is: ", key)
    return "Hi,You can enter question about blackduck below"


@app.route('/response')
def chat_response():
    api = FAQAPI()
    answer = api.ask_question(request.args.get('MessageInput'))
    print("The Question is:", request.args.get('MessageInput'))
    print("The Answer is:", answer)
    return answer
