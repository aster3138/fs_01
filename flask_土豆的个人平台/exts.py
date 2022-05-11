from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# 连接数据库，邮箱的模块

db = SQLAlchemy()
mail = Mail()