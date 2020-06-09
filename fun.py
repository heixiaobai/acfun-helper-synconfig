# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter


def authCookie(cookie: str):
    """
    传入Cookie，向官方API验证
    :param cookie: Cookie
    :return: True or False
    """
    url = "https://api-new.app.acfun.cn/rest/app/user/hasSignedIn"
    header = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2954.36 Safari/537.36",
        "Cookies": cookie
    }
    s = requests.session()
    s.mount('https://', HTTPAdapter(max_retries=2))
    try:
        r = requests.get(url=url, headers=header, timeout=(5, 5))
        if r.json()['result'] == 0:
            return True
        else:
            return False
    except Exception as e:
        print(e.args)
        import traceback
        print(traceback.format_exc())
        return False
