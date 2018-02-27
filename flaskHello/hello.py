from flask import Flask
from flask import render_template
from flask import request
from flask import url_for


app = Flask(__name__)
app.secret_key = "thisissecretkey"

from user import username
app.register_blueprint(username)

### setting environment variable:
### Windows CMD			: set FLASK_APP=hello.py
### Windows PowerShell	: $env:FLASK_APP="hello.py"
### Mac Terminal		: export FLASK_APP=hello.py


#### TESTING BluePrint functionality ####
@app.route('/hello/')
@app.route('/hello/<name>')
def hello_world(name=None):
    return 'Hello, %s!' % name

#########################################

########### Normal URL Routing ###########

@app.route('/')
def landing():
    return "<h1>Welcome to FlaskHello app!</h1>"

@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/category/')
def category():
    return render_template('category.html')

@app.route('/quiz/')
def quiz():
    return render_template('quiz.html')

#########################################


######### Testing modularity ###########

#from views1 import *
import views1

# import views contains the snippet below:
# @app.route('/input/', methods=['GET','POST'])
# def input():
# 	if request.method == 'POST':
# 		print(request.form)
# 		if('textinput' in request.form):
# 			passedvar = request.form.get('textinput')
# 		elif('optionchkbox' in request.form):
# 			passedvar = request.form.getlist('optionchkbox')
# 		elif('optionradio' in request.form):
# 			passedvar = request.form.getlist('optionradio')
# 		print("passedvar:", passedvar)
# 		return render_template('input.html.j2', passedvar = passedvar)
# 	elif request.args.get('option'):
# 		return("GET: " + request.args.get('option'))
# 	return render_template('input.html.j2')

##########################################

######### Testing FileUpload ###########
import upload
########################################

######### Testing FileUpload ###########
import textanalysis
########################################


# if using cmd: 'python hello.py'
if __name__ == '__main__':
    app.run(debug=True)