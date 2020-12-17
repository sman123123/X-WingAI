from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import sqlalchemy

app = Flask(__name__)
app.secret_key = "Some Secret Key"
app.permanent_session_lifetime = timedelta(days=1)

@app.route("/")
def home(name):
	return render_template("index.html", content=name)


if __name__ == "__main__":
	app.run()