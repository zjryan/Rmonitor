from flask import Flask


app = Flask(__name__)
app.secret_key = 'random-string'


from . import views