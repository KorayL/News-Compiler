from flask import Flask, render_template
from flaskwebgui import FlaskUI

import waitress
import webbrowser

# Create flask app and gui
app = Flask(__name__)
ui = FlaskUI(app=app, server="flask", fullscreen=False)


# Create function for main site
@app.route("/")
def index():
    return render_template("index.html")


# Create function for article site
@app.route("/article.html")
def article():
    return render_template("article.html")


# Function to run the gui
def run():
    webbrowser.open_new("http://127.0.0.1:5000")
    waitress.serve(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    run()
