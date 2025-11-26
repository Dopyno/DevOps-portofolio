# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .database import get_db
from .s3_utils import upload_orders_to_s3

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        customer_name = request.form.get("customer")
        coffee_type = request.form.get("coffee")
        size = request.form.get("size")

        if not (customer_name and coffee_type and size):
            # într-o versiune avansată: flash message + error
            return redirect(url_for("main.index"))

        db = get_db()
        db.execute(
            "INSERT INTO orders (customer_name, coffee_type, size) VALUES (?, ?, ?)",
            (customer_name, coffee_type, size),
        )
        db.commit()

        return redirect(url_for("main.index"))

    return render_template("index.html")


@bp.route("/report")
def report():
    db = get_db()
    orders = db.execute(
        "SELECT id, customer_name, coffee_type, size, created_at FROM orders ORDER BY created_at DESC"
    ).fetchall()

    # upload în S3 (dacă e configurat)
    upload_orders_to_s3(orders)

    return render_template("report.html", orders=orders)


@bp.route("/health")
def health():
    try:
        db = get_db()
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False

    return jsonify(
        {
            "status": "ok" if db_ok else "degraded",
            "database": db_ok,
        }
    )

