from flask import Flask, render_template, request

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
