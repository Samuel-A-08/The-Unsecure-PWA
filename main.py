from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import user_management as dbHandler
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)


def safe_redirect(url):
    parsed = urlparse(url)
    if parsed.netloc == "" and parsed.path.startswith("/"):
        return redirect(url)
    return redirect("/index.html")


@app.route("/success.html", methods=["GET", "POST"])
def addFeedback():
    if request.method == "GET":
        url = request.args.get("url")
        if url:
            return safe_redirect(url)
        return render_template("success.html")

    feedback = request.form.get("feedback", "")
    dbHandler.insertFeedback(feedback)
    return render_template("success.html", state=True, value="Back")


@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        url = request.args.get("url")
        if url:
            return safe_redirect(url)
        return render_template("signup.html")

    username = request.form.get("username")
    password = request.form.get("password")
    dob = request.form.get("dob")

    dbHandler.insertUser(username, password, dob)
    return render_template("index.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/index.html", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        url = request.args.get("url")
        if url:
            return safe_redirect(url)

        msg = request.args.get("msg", "")
        return render_template("index.html", msg=msg)

    username = request.form.get("username")
    password = request.form.get("password")

    if dbHandler.retrieveUsers(username, password):
        return render_template("success.html", value=username, state=True)

    return render_template("index.html")
