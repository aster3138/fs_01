from exts import db
from datetime import datetime
# 此模块用于创建数据库模型（即可通过 映射 创建数据库）
# 第一次映射的时候，需要通过 flask db init 进行实例化，之后就不再需要
# 映射的方式：终端, flask db migrate 生成迁移脚本， 然后通过 flask db upgrade 映射到数据库中


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)  # default 只在第一次存在数据库时，才会保存值，以后更新的时候，就不会变化


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)  # unique=True 代表唯一，默认False
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=False)
    join_time = db.Column(db.DateTime, default=datetime.now)


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 外键，引用UserModel模型里的id

    author = db.relationship("UserModel", backref="questions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    answer_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # question = db.relationship("QuestionModel", backref="answers")  # 通过question去访问所有的答案时，可以指定一个排序方式
    # desc()代表从大到小，order_by=create_time代表根据时间排序
    question = db.relationship("QuestionModel", backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship("UserModel", backref="answers")
