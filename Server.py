# -*- coding: utf-8 -*-
from flask import Flask, request, session
import config
import redis
import json
import fun

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = config.SESSION_LIFETIME
app.config['SESSION_REDIS'] = redis.StrictRedis(connection_pool=redis.ConnectionPool.from_url(config.REDIS_URL))
app.config['SESSION_KEY_PREFIX'] = "session:"


@app.route("/")
def index():
    return "AcFun 辅助站点"


@app.route("/api/acfun-helper/options/version", methods=['GET'])
def option_version():
    """
    接口修改后版本号变更
    :return:版本号
    """
    version_info = "bate-0.3"
    return version_info


@app.route("/api/acfun-helper/options/upload", methods=['POST'])
def upload():
    """
    上传接口，接收form-data格式的options
    :return: 返回确认或错误内容，对于未约定的出错情况，前端应该直接输出返回值
    """
    optionsJson = json.loads(request.form.get('options_data'))
    # 从options中读取cookie，因为AcPassToken被放在另一个key，所以需要拼接
    try:
        cookie = optionsJson["AcCookies"]+"; acPasstoken="+optionsJson["AcPassToken"]
    except KeyError:
        return "Cookie Error"

    # 验证用户信息是否存在于session内
    if 'uid' in session:
        # 验证通过，将options根据uid存入redis
        uid = dict(i.split("=") for i in cookie.split("; "))['auth_key']
        optionsJson.pop("AcCookies")
        optionsJson.pop("AcPassToken")
        fun.save_option(uid, json.dumps(optionsJson))
        return "OK"

    # 验证传递的acfun cookie
    elif fun.auth_cookie(cookie):
        # 验证通过，将options根据uid存入redis
        uid = dict(i.split("=") for i in cookie.split("; "))['auth_key']
        optionsJson.pop("AcCookies")
        optionsJson.pop("AcPassToken")
        fun.save_option(uid, json.dumps(optionsJson))

        # 将验证过的用户信息存入session，存活时间内请求不需要再次验证
        session['uid'] = uid
        return "OK"

    else:
        return "Auth Error"


@app.route("/api/acfun-helper/options/download", methods=['POST'])
def download():
    """
    下载接口，接收form-data格式，存在cookie和AcPassToken的dict
    :return: 返回options，UID对应的option不存在返回None
    """
    authCookie = json.loads(request.form.get('authCookie'))
    try:
        cookie = authCookie["AcCookies"]+"; acPasstoken="+authCookie["AcPassToken"]
    except KeyError:
        return "Cookie Error"

    # 验证用户信息是否存在于session内
    if 'uid' in session:
        # 验证通过，根据UID从redis读取options数据返回
        uid = dict(i.split("=") for i in cookie.split("; "))['auth_key']
        data = fun.load_option(uid)
        if data is None:
            return "None"
        else:
            return data

    elif fun.auth_cookie(cookie):
        # 验证通过，根据UID从redis读取options数据返回
        uid = dict(i.split("=") for i in cookie.split("; "))['auth_key']

        # 将验证过的用户信息存入session，存活时间内请求不需要再次验证
        session['uid'] = uid

        data = fun.load_option(uid)
        if data is None:
            return "None"
        else:
            return data

    else:
        return "Auth Error"
