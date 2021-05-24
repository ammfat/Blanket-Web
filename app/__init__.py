from flask import Flask
from flask_mysql_connector import MySQL

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

mysql = MySQL(app)

from app import views