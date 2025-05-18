from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    books = [
        {"title": "Dune", "author": "Frank Herbert", "cover": "dune.jpg", "description": "Sci-fi classic."},
        {"title": "Educated", "author": "Tara Westover", "cover": "educated.jpg", "description": "Memoir of resilience."},
        # Add more books here
    ]
    return render_template("index.html", books=books)
