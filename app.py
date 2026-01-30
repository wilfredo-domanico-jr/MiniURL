import sqlite3
import string
import random
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
DB_NAME = "urls.db"

# -------------------------
# Database setup
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -------------------------
# Generate short code
# -------------------------
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# -------------------------
# Create short URL
# -------------------------
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, short_code)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Short code collision"}), 500
    finally:
        conn.close()

    return jsonify({
        "original_url": original_url,
        "short_url": f"http://localhost:5000/{short_code}"
    })

# -------------------------
# Redirect short URL
# -------------------------
@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return jsonify({"error": "URL not found"}), 404

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
