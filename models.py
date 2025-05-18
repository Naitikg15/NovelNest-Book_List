from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover = db.Column(db.String(200), nullable=False)
    genres = db.Column(db.String(200), nullable=False)  # Comma-separated string
    favorite = db.Column(db.Boolean, default=False)

    def get_genre_list(self):
        return [g.strip() for g in self.genres.split(',')]
