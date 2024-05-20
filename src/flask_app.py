from flask import Flask, render_template
from flaskwebgui import FlaskUI

import waitress
import webbrowser

from main import main

# Create flask app and gui
app = Flask(__name__)
ui = FlaskUI(app=app, server="flask", fullscreen=False)


# Create function for main site
@app.route("/")
def index():
    """ Creates the main site. """

    return render_template("index.html")


# Create function for article site
@app.route("/article.html")
def article():

    """ Creates the article site. """
    return render_template("article.html")

@app.route("/reload")
def reload():
    """ Reloads the main site. """

    main()  # Run main function to update articles
    return render_template("index.html")

# Function to run the gui
def run():
    """ Runs the gui. """

    webbrowser.open_new("http://127.0.0.1:5000")
    waitress.serve(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    run()
