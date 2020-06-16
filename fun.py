# -*- coding: utf-8 -*-
import redis
import config
import requests
from requests.adapters import HTTPAdapter

r = redis.StrictRedis(connection_pool=redis.ConnectionPool.from_url(config.REDIS_URL))


def save_option(uid: str, options: str):
    """
    根据UID将options存入Redis
    :param uid: uid
    :param options: 字符化的dict
    :return: None
    """
    r.set("options:"+uid, options)


def load_option(uid: str):
    """
    从Redis读取UID对应的options并返回
    :param uid: UId
    :return: 字符化的dict
    """
    return r.get("options:"+uid)


def auth_cookie(cookie: str):
    """
    传入Cookie，向AcFun官方API验证用户
    :param cookie: Cookie
    :return: BOOL True or False
    """
    url = "https://api-new.app.acfun.cn/rest/app/user/hasSignedIn"
    # 需要定义header，否则会返回403
    header = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2954.36 Safari/537.36",
        "Cookie": cookie
    }

    s = requests.session()
    # 超时重试2次
    s.mount('https://', HTTPAdapter(max_retries=2))
    try:
        # 超时时间和读取超时均为5秒
        res = requests.get(url=url, headers=header, timeout=(5, 5))
        # 返回json中，result为0是正常用户，否则就是cookie有误
        if res.json()['result'] == 0:
            return True
        else:
            return False
    except Exception as e:
        # 暂时没有遇到需要处理的错误
        # TODO: 应该将错误写入error log，而不是打印
        print(e.args)
        import traceback
        print(traceback.format_exc())
        return False
