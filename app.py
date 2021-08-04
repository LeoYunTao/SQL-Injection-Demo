from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

from flask.helpers import flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    else:
        username, password = request.form["username"], request.form["password"]
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        x = cur.execute(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'").fetchall()
        con.close()
        if len(x) == 1:
            session["username"] = x[0][0]
            return redirect(url_for("home"))
        else:   
            return render_template("index.html", login=False)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", error_message=None)
    else:
        username, password, confirm_password = request.form["username"], request.form["password"], request.form["confirm_password"]
        if password != confirm_password:
            return render_template("signup.html", error_message="Error: password does not match")

        con = sqlite3.connect("data.db")
        cur = con.cursor()
        try:
            cur.executescript(f"INSERT INTO user VALUES ('{username}', '{password}')")
        except sqlite3.IntegrityError:
            con.close()
            return render_template("signup.html", error_message="Error: username alreadly exist")
        con.commit()
        con.close()
        
        flash("Sign up successful")
        return redirect(url_for("login"))

@app.route("/loginsuccessful")
def home():
    if session["username"]:
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        table = cur.execute("SELECT * FROM user").fetchall()
        con.close()
        print(table)
        return render_template("loginsuccessful.html", username=session["username"], table=table)

if __name__ == "__main__":
    app.run(debug=True)
