from hello import app

from flask import request, render_template

@app.route('/input/', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        print(request.form)
        if 'textinput' in request.form:
            passedvar = request.form.get('textinput')
        elif 'optionchkbox' in request.form:
            passedvar = request.form.getlist('optionchkbox')
        elif 'optionradio' in request.form:
            passedvar = request.form.getlist('optionradio')
        print("passedvar:", passedvar)
        return render_template('input.html.j2', passedvar=passedvar)
    elif request.args.get('option'):
        return("GET: " + request.args.get('option'))
    return render_template('input.html.j2')
