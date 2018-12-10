from flask import Flask, flash, render_template, request, redirect, url_for, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators, HiddenField
from passlib.hash import sha256_crypt
from FlaskApp.database import se_db
import sys
import gc
import json

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "super secret key"

class RegistrationForm(Form):
    firstname = TextField('First Name')
    lastname = TextField('Last Name')
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class PickClassForm(Form):
    class_list = HiddenField('Class List')

@app.route('/')
def homepage():
    return redirect(url_for("loginpage"))

@app.route('/login/', methods=["GET", "POST"])
def loginpage():
    user_db = se_db()
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST":
            email = form.email.data
            password = form.password.data
            passwordE = sha256_crypt.encrypt((str(form.password.data)))

            # Check if email exists in user db
            if (user_db.checkProfileCredentials(email, password) == True):
                flash("Welcome!")
                gc.collect()
                session['logged_in'] = True
                session['email'] = email
                user_db.closeConnection()
                return redirect(url_for('welcome_page'))
            else:
                flash("Error: Incorrect email/password")
                gc.collect()
                print("Error: Incorrect email/password")
        
        user_db.closeConnection()
        return render_template("signin.html", form=form)
    except Exception as e:
        print("Error displaying form")
        user_db.closeConnection()
        return (str(e))

@app.route('/register/', methods=["GET", "POST"])
def register_page():
    user_db = se_db()
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            password = form.password.data
            passwordE = sha256_crypt.encrypt((str(form.password.data)))
            try:
                user_db.addProfile(email, password, firstname, lastname,)
                flash("Thanks for registering!")
                gc.collect()

                session['logged_in'] = True
                session['email'] = email
                user_db.closeConnection()
                return redirect(url_for('pick_classes'))
            except:
                flash("Error: Information could not be properly inserted into database");
                gc.collect();
        user_db.closeConnection()
        return render_template('signin.html', form=form)
    except Exception as e:
        print("Error displaying form")
        user_db.closeConnection()
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
    user_db = se_db()
    user_db.closeConnection()
    return render_template("welcomepage.html")

@app.route('/pick_classes/', methods=["GET", "POST"])
def pick_classes():
    try:
        form = PickClassForm(request.form)
        if request.method == "POST":
            class_list = form.class_list.data
            classes_seperated = class_list.split(",")
            for i in range(len(classes_seperated)):
                user_db1 = se_db()
                user_db1.addUserToClass(session["email"], classes_seperated[i])
                user_db1.closeConnection()
            return redirect(url_for("welcome_page"))
        user_db = se_db()
        list_of_classes = user_db.listClasses()
        user_db.closeConnection()
        print("Test")
        return render_template("pick_classes.html", form = form, list_of_classes = list_of_classes)
    except Exception as e:
        print("Error displaying form")
        return (str(e))

if __name__ == "__main__":
    app.run()
