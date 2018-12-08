from flask import Flask, flash, render_template, request, redirect, url_for, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from FlaskApp.database import se_db
import sys
import gc

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "super secret key"
user_db = se_db()

class RegistrationForm(Form):
    firstname = TextField('First Name')
    lastname = TextField('Last Name')
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

@app.route('/')
def homepage():
    return redirect(url_for("loginpage"))

@app.route('/login/', methods=["GET", "POST"])
def loginpage():
    error = ""
    try:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            # Check if email exists in user db
            if email == "myemail@test.com" and password == "test":
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid email"

        form = RegistrationForm(request.form)
        return render_template("signin.html", form=form)
    except Exception as e:
        return render_template("signin.html", error=error)

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            user_db.addProfile(email, password, firstname, lastname,)
            flash("Thanks for registering!")
            gc.collect()

            session['logged_in'] = True
            session['email'] = email

            return redirect(url_for('welcome_page'))
        return render_template('signin.html', form=form)
    except Exception as e:
        return (str(e))

#def register_new_user():
#    error = ""
#    try:
#        if request.method == "POST":
#            firstname = request.form["firstname"]
#            lastname = request.form["lastname"]
#            email = request.form["email"]
#            password = request.form["password"]
#            password_conf = request.form["password_conf"]
#
#            # Should give user an error message about mismatching password
#            if password != password_conf:
#                return render_template("signin.html")
#            user_db.addProfile(email, password, firstname, lastname,)
#            return redirect(url_for("welcome_page"))
#        
#        return render_template("welcomepage.html")
#    except Exception as e:
#        return render_template("signin.html", error=error) 

@app.route('/welcome_page/')
def welcome_page():
    return render_template("welcomepage.html")   


if __name__ == "__main__":
    app.run()
