"""
This is flask app module for all things related
to text mining such as wordclouds, and sentiment analysis
"""
import os
import pandas as pd

from hello import app

from flask import request, render_template, flash, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '.\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/text/', methods=['GET', 'POST'])
def textanalysis():
    if request.method == 'POST':
        print(request.files)
        if 'uploaded' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        file = request.files['uploaded']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            ## Validating filename
            accepted_ext = ['.xls', '.xlsx', '.csv']
            file_name, file_ext = os.path.splitext(filename)
            if file_ext not in accepted_ext:
                flash('File Type is not supported. Please upload \
                        csv,xls,or xlsx.')
                return redirect(request.url)
            del file_name, file_ext
            fileurl = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fileurl)
            flash("Your File is uploaded! File: "+fileurl)
            print('File Location:', fileurl)

            # Process Data
            wordfreq = createwordcloud(fileurl)

            # Pass data to front-end
            return render_template('textanalysis.html', 
                                    wordcloud_wordfreq=wordfreq,
                                    fileurl=fileurl
                                    )

    return render_template('textanalysis.html')

def createwordcloud(fileurl=None):
    """ create wordcloud """
    print("*** Wordcloud Creation ***")
    file_name, file_ext = os.path.splitext(os.path.basename(fileurl))

    if file_ext == '.csv':
        ## read csv
        wordfile = pd.read_csv(fileurl)
    elif file_ext == '.xls':
        ## read xls
        xls = pd.ExcelFile(fileurl)
        wordfile = xls.parse(0)
    elif file_ext == '.xlsx':
        ## read xlsx
        wordfile = pd.read_excel(fileurl, sheet_name=0)
      
    print(wordfile.info())

    # Count words and freqs
    textstringlist = wordfile['comment_clean'][:5]
    
    # Combine wordlist into a string
    textstring = ' '.join(textstringlist)
    # cleanup string
    textstring = textstring.lower().replace('#livechatwithhamish', '')
    from string import punctuation
    for p in punctuation:
        textstring =textstring.replace(p,'')
    
    # Count wordfreq
    from collections import Counter
    wordcount = Counter(textstring.split())

    # Create list of list object of wordfreq
    wordfreq = []
    for content in list(wordcount.items()):
        temp = [content[0], content[1]]
        wordfreq.append(temp)
    del temp


    print("*** End Wordcloud ***")
    return wordfreq