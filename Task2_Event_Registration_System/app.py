from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "codealpha_event_registration_secret"  # needed for flash messages

DATABASE = "database.db"


EVENTS = [
    {
        "id": 1,
        "title": "Tech Innovators Summit",
        "date": "2026-08-12",
        "venue": "Chennai Trade Centre",
        "description": "A gathering of developers, founders, and product "
                        "teams discussing the latest in AI and cloud tech.",
    },
    {
        "id": 2,
        "title": "Campus Hackathon 2026",
        "date": "2026-09-05",
        "venue": "Easwari Engineering College, Auditorium",
        "description": "24-hour hackathon for students to build and pitch "
                        "projects across web, AI, and IoT tracks.",
    },
    {
        "id": 3,
        "title": "Career Readiness Workshop",
        "date": "2026-09-20",
        "venue": "Online (Zoom)",
        "description": "Resume reviews, mock interviews, and guidance on "
                        "cracking SDE-1 roles at product companies.",
    },
]


def get_event(event_id):
    """Look up an event by id from the hardcoded list. Returns None if missing."""
    return next((e for e in EVENTS if e["id"] == event_id), None)



# Database setup — only registrations are persisted; events stay hardcoded.

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            registered_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


init_db()



@app.route("/")
def index():
    return render_template("index.html", events=EVENTS)


@app.route("/event/<int:event_id>")
def event_detail(event_id):
    event = get_event(event_id)
    if event is None:
        return "<h2>Event not found!</h2>", 404
    return render_template("event.html", event=event)


@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):
    event = get_event(event_id)
    if event is None:
        return "<h2>Event not found!</h2>", 404

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

     
        if not name or not email:
            flash("Both name and email are required.")
            return render_template("register.html", event=event)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO registrations (event_id, name, email) VALUES (?, ?, ?)",
            (event_id, name, email)
        )
        conn.commit()
        conn.close()

        flash(f"You're registered for {event['title']}!")
        return redirect(url_for("index"))

    return render_template("register.html", event=event)


if __name__ == "__main__":
    app.run(debug=True)