import os
import uuid
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

db = SQLAlchemy()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def create_app():
    app = Flask(__name__)

    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

    instance_name = os.getenv("INSTANCE", "unknown-instance")

    # DB în /data ca să îl montăm volume shared
    db_path = os.getenv("DB_PATH", "/data/app.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

    uploads_dir = Path(os.getenv("UPLOAD_DIR", "/uploads"))
    uploads_dir.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    class Movie(db.Model):
        __tablename__ = "movies"
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False, index=True)
        year = db.Column(db.Integer, nullable=True)
        genre = db.Column(db.String(120), nullable=True)
        poster_filename = db.Column(db.String(255), nullable=True)

        def to_dict(self):
            return {
                "id": self.id,
                "title": self.title,
                "year": self.year,
                "genre": self.genre,
                "poster_url": f"/uploads/{self.poster_filename}" if self.poster_filename else None,
            }

    with app.app_context():
        db.create_all()

    def allowed_file(filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_poster(file_storage):
        if not file_storage or file_storage.filename == "":
            return None
        filename = secure_filename(file_storage.filename)
        if not allowed_file(filename):
            return None
        ext = filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        file_storage.save(str(uploads_dir / unique_name))
        return unique_name

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", instance=instance_name)

    @app.get("/api/movies")
    def list_movies():
        q = (request.args.get("q") or "").strip()
        query = Movie.query
        if q:
            query = query.filter(Movie.title.ilike(f"%{q}%"))
        movies = query.order_by(Movie.id.desc()).all()
        return jsonify(instance=instance_name, items=[m.to_dict() for m in movies])

    @app.post("/api/movies")
    def create_movie():
        # multipart/form-data: title, year, genre, poster(file)
        title = (request.form.get("title") or "").strip()
        year_raw = (request.form.get("year") or "").strip()
        genre = (request.form.get("genre") or "").strip()

        if not title:
            return jsonify(error="title is required", instance=instance_name), 400

        poster_file = request.files.get("poster")
        poster_filename = None
        if poster_file and poster_file.filename:
            poster_filename = save_poster(poster_file)
            if poster_filename is None:
                return jsonify(error="invalid poster type (png/jpg/jpeg/webp)", instance=instance_name), 400

        movie = Movie(
            title=title,
            year=int(year_raw) if year_raw.isdigit() else None,
            genre=genre or None,
            poster_filename=poster_filename,
        )
        db.session.add(movie)
        db.session.commit()

        return jsonify(instance=instance_name, item=movie.to_dict()), 201

    @app.delete("/api/movies/<int:movie_id>")
    def delete_movie(movie_id: int):
        movie = Movie.query.get(movie_id)
        if not movie:
            return jsonify(error="not found", instance=instance_name), 404

        # șterge fișierul poster
        if movie.poster_filename:
            path = uploads_dir / movie.poster_filename
            if path.exists():
                try:
                    path.unlink()
                except OSError:
                    pass

        db.session.delete(movie)
        db.session.commit()
        return jsonify(status="deleted", instance=instance_name)

    # Servire poze uploadate
    @app.get("/uploads/<path:filename>")
    def uploaded_file(filename):
        # edge-nginx va proxya la backend pentru /uploads/*
        return send_from_directory(str(uploads_dir), filename, as_attachment=False)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
