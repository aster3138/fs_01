# 数据库的配置信息
# HOSTNAME = '127.0.0.1'
# PORT     = '3306'
# DATABASE = "tudou_personal_platform"
# USERNAME = 'root'
# PASSWORD = '111111'
DB_URL = "mysql+pymysql://root:111111@127.0.0.1:3306/tudou_personal_platform?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URL

SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'fafafsgsgshgrdhy'

# 邮箱配置
# 我们项目中用的是qq邮箱
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "930916977@qq.com"
MAIL_PASSWORD = "awykbvfsoarcbchg"
MAIL_DEFAULT_SENDER = "930916977@qq.com"

