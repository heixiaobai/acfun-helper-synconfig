# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import fun

app = Flask(__name__)


@app.route("/")
def index():
    return "Test"


@app.route("/api/auth", methods=['POST'])
def auth():
    if fun.authCookie(request.form.get('Cookie')):
        return "Yes"
    else:
        return "No"
