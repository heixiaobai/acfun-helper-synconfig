# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import fun

app = Flask(__name__)


@app.route("/")
def index():
    return "Test"


@app.route("/api/option", methods=['POST'])
def auth():
    # print(request.form.get('Cookie'))
    cookie = request.form.get('Cookie')
    print(type(request.form.get('Cookie')))

    # 验证传递的cookie
    if fun.auth_cookie(cookie):
        uid = dict(i.split("=") for i in cookie.split("; "))['auth_key']
        options = request.form.get('options_data')
        fun.save_option(uid, options)
        return "Yes"
    else:
        return "Auth Error"
