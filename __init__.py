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
            attempted_email = request.form["signin-email"]
            attempted_password = request.form["signin-pw"]

            if attempted_email == "myemail@test.com":
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid email"

        return render_template("signin.html")
    except Exception as e:
        return render_template("signin.html", error=error)

if __name__ == "__main__":
    app.run()
