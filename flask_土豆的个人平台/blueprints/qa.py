from flask import Blueprint, render_template, g, request, redirect, url_for, flash
from decorators import login_require
from .forms import QuestionForm, AnswerForm
from models import QuestionModel,AnswerModel
from exts import db
from sqlalchemy import or_

# 用户问答蓝图,各种视图函数 模块

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    # 查询QuestionModel数据库里所有的数据，questions相当于列表
    # order_by("create_time")把数据根据时间排序,顺序是从小往大排
    # 我们要排倒序，可以这样order_by(db.text("-create_time"))

    return render_template("index.html", questions=questions)


@bp.route("/question/public", methods=['GET', 'POST'])
@login_require  # 装饰器函数
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question_msg = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question_msg)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误！")
            return redirect(url_for("qa.public_question"))

# @login_require  # 装饰器函数
# def public_question():
#     return render_template("public_question.html")
# 等价于 login_require(public_question)
# 装饰器函数的作用：把函数public_question 当成参数传入到函数 login_require（）里，然后返回函数wrapper()
# 返回函数wrapper() 之后再执行函数 wrapper()， 进行判断用户是否登录


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template("detail.html", question=question)


@bp.route("/answer<int:question_id>", methods=["POST"])  # 通过url传递参数question_id
@login_require
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        # question_id = form.question_id.data   # 不需要从表单获取数据了
        answer_model = AnswerModel(content=content, question_id=question_id, author=g.user)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for("qa.question_detail", question_id=question_id))
    else:
        flash("表单验证失败！")
        return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route("/search")
def search():
    # /search?q=xxxx
    q = request.args.get("q")
    # filter_by: 直接使用字段的名称
    # filter: 使用模型.字段的名称
    questions =QuestionModel.query.filter(or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q))).order_by(db.text("-create_time"))
    return render_template("index.html", questions=questions)






