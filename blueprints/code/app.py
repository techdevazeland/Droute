from flask import Blueprint

app = Blueprint('app', __name__)
code = '''
SIN APP
'''
@app.route('/')
def app_home():
    return code