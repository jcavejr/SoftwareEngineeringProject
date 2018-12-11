from flask import Flask, flash, render_template, request, redirect, url_for, session
from wtforms import Form, BooleanField, TextField, PasswordField, validators, HiddenField, SelectField, TextAreaField
from passlib.hash import sha256_crypt
from FlaskApp.database import se_db
import sys
import gc
import json

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "super secret key"

user_db = se_db()
select_field_classes = []
list_of_classes_global = user_db.listClasses()
select_field_classes = []
for i in range(len(list_of_classes_global)):
    class_tuple = (list_of_classes_global[i], list_of_classes_global[i])
    select_field_classes.append(class_tuple)
user_db.closeConnection()


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

class AskQuestionForm(Form):
    title = TextField('Title')
    post = TextAreaField('Message')
    class_name = SelectField('Class', choices=select_field_classes)

class AnswerQuestionForm(Form):
    answer = TextAreaField('Help us answer this question!')



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
                user_db.addDateTime(session['email'])
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

@app.route('/welcome_page/')
def welcome_page():
    form = AskQuestionForm(request.form)
    formAnswer = AnswerQuestionForm(request.form)
    user_db = se_db()
    title_list = user_db.getThreadTitlesByTime()
    creator_list = user_db.getThreadCreatorByTime()
    post_list = user_db.getThreadMessageByTime()
    active_users = user_db.getActiveUsers()
    thread_nums = user_db.getThreadNumbersByTime()
    name = user_db.getProfileName(session['email'])
    classes = user_db.getProfileClasses(session['email'])
    replies1 = user_db.getRepliesToThread(int(float(thread_nums[0])))
    replies2 = user_db.getRepliesToThread(int(float(thread_nums[1])))
    replies3 = user_db.getRepliesToThread(int(float(thread_nums[2])))
    user_db.closeConnection()

    user_db1 = se_db()
    user_db1.addDateTime(session['email'])
    user_db1.closeConnection()
    return render_template("welcomepage.html", form = form, formAnswer = formAnswer, title_list = title_list, creator_list = creator_list, post_list = post_list, active_users = active_users, name = name, thread_nums = thread_nums, replies1 = replies1, replies2 = replies2, replies3 = replies3, classes = classes)

@app.route('/pick_classes/', methods=["GET", "POST"])
def pick_classes():
    try:
        form = PickClassForm(request.form)
        if request.method == "POST":
            class_list = form.class_list.data
            classes_seperated = class_list.split(",")
            for i in range(len(classes_seperated)):
                user_db1 = se_db()
                try:
                    user_db1.addUserToClass(session["email"], classes_seperated[i])
                    user_db1.closeConnection()

                    user_db2 = se_db()
                    user_db2.addDateTime(session['email'])
                    user_db2.closeConnection()
                except:
                    flash("Error: Information could not be properly inserted into database");
                    gc.collect();
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

@app.route('/create_new_post/', methods=["GET", "POST"])
def create_new_post():
    try:
        form = AskQuestionForm(request.form)
        if request.method == "POST":
            user_db = se_db()

            title = form.title.data
            body = form.post.data
            class_name = form.class_name.data
            try:
                user_db.addMessage(0, 0, session["email"], title, body, class_name)
                user_db.closeConnection()
                
                user_db1 = se_db()
                user_db1.addDateTime(session['email'])
                user_db1.closeConnection()
            except:
                flash("Error: Information could not be properly inserted into database");
                gc.collect();
                user_db.closeConnection()
            return redirect(url_for("welcome_page"))
        return render_template("welcomepage.html", form = form)
    except Exception as e:
        print("Error displaying form")
        return (str(e))

@app.route('/1/', methods=["GET", "POST"])
def reply1():
    user_db = se_db()
    title_list = user_db.getThreadTitlesByTime()
    thread_nums = user_db.getThreadNumbersByTime()
    replies1 = user_db.getRepliesToThread(int(float(thread_nums[0])))
    user_db.closeConnection()
    try:
        form = AnswerQuestionForm(request.form)
        if request.method == "POST":
            answer = form.answer.data
            try:
                user_db1 = se_db()
                try:
                    user_db1.addMessage(1, (float(thread_nums[0])+len(replies1)/1000), session["email"], title_list[0], answer, "C")
                except Exception as e:
                    print(e)
                user_db1.closeConnection()
            except:
                flash("Error: Information could not be properly inserted into database");
                gc.collect();
            return redirect(url_for("welcome_page"))
        return render_template("welcomepage.html", form = form)
    except Exception as e:
        print("Error displaying form")
        return (str(e))

@app.route('/2/', methods=["GET", "POST"])
def reply2():
    user_db = se_db()
    title_list = user_db.getThreadTitlesByTime()
    thread_nums = user_db.getThreadNumbersByTime()
    replies2 = user_db.getRepliesToThread(int(float(thread_nums[1])))
    user_db.closeConnection()
    try:
        form = AnswerQuestionForm(request.form)
        if request.method == "POST":
            answer = form.answer.data
            try:
                user_db1 = se_db()
                try:
                    user_db1.addMessage(1, (float(thread_nums[1])+len(replies2)/1000), session["email"], title_list[1], answer, "C")
                except Exception as e:
                    print(e)
                user_db1.closeConnection()
            except:
                flash("Error: Information could not be properly inserted into database");
                gc.collect();
            return redirect(url_for("welcome_page"))
        return render_template("welcomepage.html", form = form)
    except Exception as e:
         print("Error displaying form")
         return (str(e))

@app.route('/3/', methods=["GET", "POST"])
def reply3():
    user_db = se_db()
    title_list = user_db.getThreadTitlesByTime()
    thread_nums = user_db.getThreadNumbersByTime()
    replies3 = user_db.getRepliesToThread(int(float(thread_nums[2])))
    user_db.closeConnection()
    try:
        form = AnswerQuestionForm(request.form)
        if request.method == "POST":
            answer = form.answer.data
            try:
                user_db1 = se_db()
                try:
                    user_db1.addMessage(1, (float(thread_nums[2])+len(replies3)/1000), session["email"], title_list[2], answer, "C")
                except Exception as e:
                    print(e)
                user_db1.closeConnection()
            except:
                flash("Error: Information could not be properly inserted into database");
                gc.collect();
            return redirect(url_for("welcome_page"))
        return render_template("welcomepage.html", form = form)
    except Exception as e:
        print("Error displaying form")
        return (str(e))


if __name__ == "__main__":
    app.run()
