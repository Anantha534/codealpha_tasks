from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# Generate random 6-character code
def generate_code():
    return ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=6
    ))

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Create short URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    long_url = request.form["url"]
    short_code = generate_code()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
        (short_code, long_url)
    )

    conn.commit()
    conn.close()

    short_url = f"http://127.0.0.1:5000/{short_code}"
    return render_template("index.html", short_url=short_url)

# Redirect to original URL
@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT long_url FROM urls WHERE short_code = ?",
        (short_code,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])

    return "<h2>URL not found!</h2>"

if __name__ == "__main__":
    app.run(debug=True)