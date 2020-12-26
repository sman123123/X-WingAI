from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from probability import Probability
#from second import second



app = Flask(__name__)
#app.register_blueprint(second, url_prefix="")
app.secret_key = "Stuart is smrat"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=1)

db = SQLAlchemy(app)

class Users(db.Model):
	_id = db.Column("id", db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))

	def __init__(self, name, email):
		self.name = name
		self.email = email

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route("/home")
@app.route("/")
def index():
	return render_template("index.html", page="home")

@app.route("/view")
def view():
	return render_template("view.html", values=Users.query.all())

@app.route("/probability", methods=["GET", "POST"])
def probabilityPage():
	if request.method == "POST":
		n = int(request.form["n"])
		n = 10 if n > 10 else n
		r = int(request.form["r"])
		r = 10 if r > 10 else n
		p = request.form["p"]
		sp = p.split("/")
		sp = int(sp[0])/int(sp[1])
		prob = Probability(n, r, sp)
		return render_template("probability.html", page="probability", n=n, r=r, p=p, prob=prob)
	else:
		return render_template("probability.html", page="probability")

@app.route("/construction")
def construction():
	return render_template("construction.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = request.form["nm"]
		session["user"] = user
		session.permanent = True
		found_user = Users.query.filter_by(name=user).first()
		if found_user:
			session["email"] = found_user.email
		else:
			usr = Users(user, "")
			db.session.add(usr)
			db.session.commit()
		return redirect(url_for("user"))
	else:
		if "user" in session:
			return redirect(url_for("user"))
		return render_template("login.html", page="login")

@app.route("/user", methods=["GET", "POST"])
def user():
	email = None
	if "user" in session:
		user = session["user"]
		if request.method == "POST":
			email = request.form["email"]
			session["email"] = email
			found_user = Users.query.filter_by(name=user).first()
			found_user.email = email
			db.session.commit()
			flash("EMail saved!", "info")
		else:
			if "email" in session:
				email = session["email"]
		return render_template("user.html", page="user", user=user, email=email)
	else:
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	session.pop("user", None)
	flash("You have been logged out!", "info")
	return redirect(url_for("index"))


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)