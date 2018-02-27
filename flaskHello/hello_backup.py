from flask import Flask
from flask import render_template
from flask import request
import pyodbc

app = Flask(__name__)

### setting environment variable:
### Windows CMD			: set FLASK_APP=hello.py
### Windows PowerShell	: $env:FLASK_APP="hello.py"
### Mac Terminal		: export FLASK_APP=hello.py

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/category/')
def category():
    return render_template('category.html')

@app.route('/quiz/')
def quiz():
    return render_template('quiz.html')

@app.route('/input/', methods=['GET','POST'])
def input():
    if request.method == 'POST':
        print(request.form)
        if('textinput' in request.form):
            passedvar = request.form.get('textinput')
        elif('optionchkbox' in request.form):
            passedvar = request.form.getlist('optionchkbox')
        elif('optionradio' in request.form):
            passedvar = request.form.getlist('optionradio')
        print("passedvar:", passedvar)
        return render_template('input.html.j2', passedvar = passedvar)
    elif request.args.get('option'):
        return("GET: " + request.args.get('option'))
    return render_template('input.html.j2')


if __name__ == '__main__':
    app.run(debug=True)