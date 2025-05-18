from flask import Flask, render_template, request, redirect, url_for
import os
from models import db, Book
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


# Predefined valid genres for dropdown and filtering
VALID_GENRES = {"Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Adventure", "Self-Help"}

# Sample book data (replace with DB later)
# books = [
#     {
#         "title": "Dune",
#         "author": "Frank Herbert",
#         "cover": "dune.jpg",
#         "description": "Sci-fi classic.",
#         "genre": ["Sci-Fi", "Adventure"],
#         "favorite": False
#     },
#     {
#         "title": "Educated",
#         "author": "Tara Westover",
#         "cover": "educated.jpg",
#         "description": "Memoir of resilience.",
#         "genre": ["Non-Fiction", "Biography"],
#         "favorite": False
#     },
#     {
#         "title": "Atomic Habits",
#         "author": "James Clear",
#         "cover": "atomic.jpg",
#         "description": "A guide to habit building.",
#         "genre": ["Non-Fiction", "Self-Help"],
#         "favorite": False
#     },
# ]

@app.route("/")
def index():
    genre_filter = request.args.get('genre')
    books = Book.query.all()

    if genre_filter:
        books = [b for b in books if genre_filter.lower() in (g.lower() for g in b.get_genre_list())]

    return render_template("index.html", books=books, genre_filter=genre_filter)

@app.route("/favorites")
def favorites():
    favorite_books = [b for b in books if b.get('favorite')]
    return render_template("favorites.html", books=favorite_books)

@app.route("/upload", methods=["GET", "POST"])
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        genres = request.form.getlist('genre')
        file = request.files['cover']

        if file and genres:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            book = Book(
                title=title,
                author=author,
                description=description,
                cover=file.filename,
                genres=",".join(genres),
                favorite=False
            )
            db.session.add(book)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template("upload.html")

@app.route("/toggle_favorite/<int:book_id>", methods=["POST"])
def toggle_favorite(book_id):
    book = Book.query.get_or_404(book_id)
    book.favorite = not book.favorite
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
