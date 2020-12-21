from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from probability import Probability
#from second import second
import os


app = Flask(__name__)
#app.register_blueprint(second, url_prefix="")
app.secret_key = "Stuart is smrat"
app.permanent_session_lifetime = timedelta(days=1)

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
		return redirect(url_for("user"))
	else:
		if "user" in session:
			return redirect(url_for("user"))
		return render_template("login.html", page="login")

@app.route("/user")
def user():
	if "user" in session:
		user = session["user"]
		return f"<h1>{user}</h1>"
	else:
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	session.pop("user", None)
	flash("You have been logged out!", "info")
	return redirect(url_for("login"))

if __name__ == "__main__":
	app.run(debug=True)