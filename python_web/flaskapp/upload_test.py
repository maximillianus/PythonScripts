import os
import time #for getTS - javascript expirer
from helloworld import app

from flask import request, render_template, flash, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '.\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getTS():
    return time.time()
app.jinja_env.globals.update(getTS=getTS)

@app.route('/upload_test/', methods=['GET', 'POST'])
def fileupload_test():
    filename = None
    if request.method == 'POST':
        if 'uploaded' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        file = request.files['uploaded']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            fileurl = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fileurl)
            print('File Location:', fileurl)
    return render_template('fileupload_test.html', filename=filename)