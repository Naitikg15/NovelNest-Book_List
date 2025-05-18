from models import db, Book
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Predefined valid genres for dropdown and filtering
VALID_GENRES = [
    "Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Adventure", "Self-Help",
    "Fantasy", "Mystery", "Thriller", "Romance", "Historical", "Horror",
    "Poetry", "Science", "Philosophy", "Classic", "Children", "Young Adult", "Graphic Novel"
]


@app.route("/")
def index():
    genre_filter = request.args.get('genre')
    books = Book.query.all()
    filtered_books = books

    if genre_filter:
        filtered_books = [b for b in books if genre_filter.lower() in (g.lower() for g in b.get_genre_list())]

    return render_template("index.html", books=filtered_books, genre_filter=genre_filter)

@app.route("/favorites")
def favorites():
    favorite_books = [b for b in books if b.get('favorite')]
    return render_template("favorites.html", books=favorite_books)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        selected_genres = request.form.getlist('genre')  # Handles multiple selected options

        # Validate and normalize genres
        genres = [g for g in selected_genres if g in VALID_GENRES]

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
        else:
            return "Invalid input. Please upload a cover and select valid genre(s).", 400

    return render_template("upload.html")

@app.route("/toggle_favorite/<title>", methods=["POST"])
def toggle_favorite(title):
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
