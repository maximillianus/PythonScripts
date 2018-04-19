from flask import Flask, render_template
from flask import request, url_for
from flask import redirect

app = Flask(__name__)
app.secret_key='thisissecret'

@app.route("/")
def hello():
	return redirect(url_for('sankeylanding'))
    #return render_template('index.html')

## For Sankey page
@app.route('/sankey_landing/')
def sankeylanding():
    return render_template('sankey_landing.html')

@app.route('/sankey_detail/')
def sankeydetail():
    return render_template('sankey_detail.html')


#### File Upload ####
import upload
##################### 

#### File Upload Test ####
import upload_test
##########################


if __name__ == "__main__":
    app.run(debug=True)
