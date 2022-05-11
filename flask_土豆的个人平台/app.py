from flask import Flask, session, g
import config
from exts import db, mail
from blueprints import qa_bp
from blueprints import user_bp
from flask_migrate import Migrate
from models import UserModel


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)


app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g, "user", user)     # setattr()给什么属性绑定什么样的变量
            g.user = user
        except:
            g.user = None


# 请求来了  ->执行 before_request -> 执行视图函数 -> 视图函数中返回模板  -> 执行context_processor


@app.context_processor   # 上下文处理器, 渲染的所有模板，都会执行这个函数
def context_processor():
    if hasattr(g, "user"):   # hasattr判断g是否有user这个属性
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run(port=8000)
