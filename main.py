from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__, template_folder="/templates")
app.secret_key = "Some Secret Key"
app.permanent_session_lifetime = timedelta(days=1)

@app.route("/home")
@app.route("/")
def index():
	return render_template("templates/index.html", page="home")

@app.route("/test")
def test():
	return render_template("templates/test.html", page="test")

@app.route("/construction")
def construction():
	return render_template("templates/construction.html")

if __name__ == "__main__":
	app.run(debug=True)