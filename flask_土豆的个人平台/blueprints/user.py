from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
# 用户相关模块，实现登录注册，登出，获得验证码 功能


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for("user.login"))
        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for("user.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        print("请求方式get")
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)  # request.form会存储前端form表单上传上来的数据
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data

            # 密码加密，md5
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            print("把用户添加进数据库")
            return redirect(url_for("user.login"))
        else:
            print("验证失败")
            return redirect(url_for("user.register"))


@bp.route("/logout")
def logout():
    # 清除session中所有的数据
    session.clear()
    return redirect(url_for('user.login'))


@bp.route("/captcha", methods=['POST'])   # 验证码
def get_captcha():
    email = request.form.get("email")   # get方式传递参数，要在url后面 ? 加上 email=邮箱地址
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    print(captcha)
    if email:
        message = Message(
            subject="邮箱测试",
            recipients=[email],
            body=f"【土豆的个人平台】您的注册验证码是：{captcha}, 请不要告诉他人！",
        )
        mail.send(message)   # 发送邮件
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()  # 查询验证码，并赋值给captcha_model
        if captcha_model:   # 如果验证码存在
            captcha_model.captcha = captcha   # 修改验证码
            captcha_model.create_time = datetime.now()  # 修改时间
            db.session.commit()                   # 提交操作
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return jsonify({"code": 200})  # code:200, 代表成功的、正常的请求
    else:
        return jsonify({"code": 400, "message": "请先传递邮箱！"})  # code:400, 代表客户端错误
