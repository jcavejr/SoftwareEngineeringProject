from flask import Flask, render_template
import sys

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/login/', methods=["GET", "POST"])
def loginpage():
    return render_template("login.html")

if __name__ == "__main__":
    app.run()
