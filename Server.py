# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import json
import fun

app = Flask(__name__)


@app.route("/")
def index():
    return "Test"


@app.route("/api/option", methods=['POST'])
def auth():
    # print(request.form.get('Cookie'))
    optionsJson = json.loads(request.form.get('options_data'))
    cookie = optionsJson["AcCookies"]
    # print(cookie)
    # print(type(request.form.get('Cookie')))

    # 验证传递的cookie
    if fun.auth_cookie(cookie):
        uid = dict(i.split("=") for i in cookie.split("; "))['auth_key']
        optionsJson.pop("AcCookies")
        optionsJson.pop("AcpushList1")
        fun.save_option(uid, json.dumps(optionsJson))
        return "OK"
    else:
        return "Auth Error"
