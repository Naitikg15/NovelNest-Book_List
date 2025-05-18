from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Sample book data (to be replaced with a database later)
books = [
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "cover": "dune.jpg",
        "description": "Sci-fi classic.",
        "genre": ["Sci-Fi", "Adventure"],
        "favorite": False
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "cover": "educated.jpg",
        "description": "Memoir of resilience.",
        "genre": ["Non-Fiction", "Biography"],
        "favorite": False
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "cover": "atomic.jpg",
        "description": "A guide to habit building.",
        "genre": ["Non-Fiction", "Self-Help"],
        "favorite": False
    },
]

@app.route("/")
def index():
    genre_filter = request.args.get('genre')
    filtered_books = books

    if genre_filter:
        filtered_books = [b for b in books if genre_filter.lower() in (g.lower() for g in b['genre'])]

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
        genre = request.form['genre'].split(',')
        file = request.files['cover']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            books.append({
                "title": title,
                "author": author,
                "cover": file.filename,
                "description": description,
                "genre": [g.strip() for g in genre],
                "favorite": False
            })
            return redirect(url_for('index'))
    return render_template("upload.html")

@app.route("/toggle_favorite/<title>")
def toggle_favorite(title):
    for book in books:
        if book['title'] == title:
            book['favorite'] = not book.get('favorite', False)
            break
    return redirect(url_for('index'))

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
