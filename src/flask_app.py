from flask import Flask, render_template
from flaskwebgui import FlaskUI


# Create flask app and gui
app = Flask(__name__)
ui = FlaskUI(app=app, server="flask", fullscreen=True)


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
    ui.run()


if __name__ == "__main__":
    ui.run()
