from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


Config = {
  "apiKey": "AIzaSyAWOOeRda97AgczMYIyHmPJqY8eRYpNnH0",
  "authDomain": "adeem-individual-project.firebaseapp.com",
  "projectId": "adeem-individual-project",
  "storageBucket": "adeem-individual-project.appspot.com",
  "messagingSenderId": "941529737600",
  "appId": "1:941529737600:web:2c2ff247c9ec6e6570b965",
  "databaseURL":"https://adeem-individual-project-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": request.form['fullname'], "username": request.form['username']}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('start'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    else:
        return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('start'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/start')
def start():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("start.html", username=user['username'])


@app.route('/clothes')
def clothes():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("clothes.html", username=user['username'])

@app.route('/makeup')
def makeup():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("makeup.html", username=user['username'])


@app.route('/skincare')
def skincare():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("skincare.html", username=user['username'])


@app.route('/shoes')
def shoes():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("shoes.html", username=user['username'])


@app.route('/accessories')
def accessories():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("accessories.html", username=user['username'])
 
# @app.route('/signout')
# def signout():
#     login_session['user'] = None
#     auth.current_user = None
#     return redirect(url_for('signin'))

# @app.route('/signout', methods=['GET', 'POST'])
# def sign():
#     error = ""
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             login_session['user'] = auth.create_user_with_email_and_password(email, password)
#             UID = login_session['user']['localId']
#             user = {"name": request.form['fullname'], "username": request.form['username']}
#             db.child("Users").child(UID).set(user)
#             return redirect(url_for('start'))
#         except:
#             error = "Authentication failed"
#             return render_template("signup.html")
#     else:
#         return render_template("signup.html")



#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)