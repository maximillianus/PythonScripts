from flask import Blueprint

username = Blueprint('user_page', __name__)

@username.route('/user/', defaults={'username':'index'})
@username.route("/user/<username>")
def userlist(username):
    return "page is %s" % username
