"""Main app module"""
from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
import routes  # pylint: disable=C0413,W0611
