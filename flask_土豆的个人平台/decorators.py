from flask import g, redirect, url_for
from functools import wraps
# 装饰器模块


def login_require(func):
    # @wraps()这个装饰器不能忘记写
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):       # 判断是否登录，如果没有登录，跳转到登录页面
            return func(*args, **kwargs)
        else:
            return redirect(url_for("user.login"))
    return wrapper
