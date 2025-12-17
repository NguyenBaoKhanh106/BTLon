from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = "sadadadadaddgssnaff"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root@localhost/karaokedb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8

login = LoginManager(app)

db = SQLAlchemy(app)
