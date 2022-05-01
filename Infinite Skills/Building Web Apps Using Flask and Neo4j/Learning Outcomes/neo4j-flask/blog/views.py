from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    data = [{"x": 1}, {"x": 3}, {"x": 5}]
    message = "This is a GET request."

    if request.method == "POST":
        message = "This is a POST request."
    return render_template("index.html", message=message, data=data)

@app.route('/about/<something>')
def about(something):
    return 'The page is about {0}'.format(something)

@app.route("/register", methods=["GET", "POST"])
def register():
    return "TODO"


@app.route("/login")
def login():
    return "TODO"


@app.route("/add_post")
def add_post():
    return "TODO"


@app.route("/like_post/<post_id>")
def like_post(post_id):
    return "TODO"


@app.route("/profile/<username>")
def profile(username):
    return "TODO"


@app.route("/logout")
def logout():
    return "TODO"