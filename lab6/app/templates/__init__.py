from flask import Flask
from app import views

app = Flask(__name__)
app.secret_key = b"secret"