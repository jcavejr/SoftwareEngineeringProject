from flask import Flask, render_template, request, redirect
import sys

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/login/', methods=["GET", "POST"])
def loginpage():
    error = ""
    try:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            # Check if email exists in user db
            if email == "myemail@test.com":
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid email"

        return render_template("signin.html")
    except Exception as e:
        return render_template("signin.html", error=error)

@app.route('/register_new_user/', methods=["GET", "POST"])
def register_new_user():
    error = ""
    try:
        if request.method == "POST":
            print("POSTING login page")
            
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            email = request.form["email"]
            password = request.form["password"]
            password_conf = request.form["password_conf"]

            if password != password_conf:
                error = "Passwords do not match"
            # Check if somebody alreadt registered with that email
            elif email == "myemail@test.com":
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid email"

        return render_template("signin.html")
    except Exception as e:
        return render_template("signin.html", error=error)    


if __name__ == "__main__":
    app.run()
