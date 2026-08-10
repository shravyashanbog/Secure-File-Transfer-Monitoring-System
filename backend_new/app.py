from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import os
import hashlib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "secure_file_transfer.db"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = "sftms_secret_key"


def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def calculate_hash(filepath):

    sha = hashlib.sha256()

    with open(filepath, "rb") as f:

        while True:

            data = f.read(4096)

            if not data:
                break

            sha.update(data)

    return sha.hexdigest()


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    conn = get_connection()

    files = conn.execute("""
        SELECT *
        FROM files
        ORDER BY id DESC
    """).fetchall()

    total_files = len(files)

    secure_transfers = sum(
        1 for f in files
        if f["status"] == "Secure"
    )

    threats_blocked = sum(
        1 for f in files
        if f["status"] == "Threat"
    )

    storage_used = sum(
        f["filesize"] or 0
        for f in files
    )

    conn.close()

    return render_template(
        "dashboard.html",
        files=files,
        total_files=total_files,
        secure_transfers=secure_transfers,
        threats_blocked=threats_blocked,
        storage_used=storage_used
    )


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    if file.filename == "":
        return redirect("/dashboard")

    save_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(save_path)

    filesize = os.path.getsize(save_path)

    filehash = calculate_hash(save_path)

    conn = get_connection()

    conn.execute("""
        INSERT INTO files
        (
            filename,
            filepath,
            filesize,
            filehash,
            status,
            integrity,
            risk_level,
            username,
            upload_time
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        file.filename,
        save_path,
        filesize,
        filehash,
        "Secure",
        "Verified",
        "LOW",
        "shravya",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()

    conn.close()

    return redirect("/dashboard")


@app.route("/api/file-status")
def file_status():

    conn = get_connection()

    files = conn.execute("""
        SELECT *
        FROM files
        ORDER BY id DESC
    """).fetchall()

    events = conn.execute("""
        SELECT *
        FROM file_events
        ORDER BY id DESC
        LIMIT 20
    """).fetchall()

    conn.close()

    return jsonify({

        "files": [
            dict(f)
            for f in files
        ],

        "events": [
            dict(e)
            for e in events
        ]

    })


@app.route("/audit-logs")
def audit_logs():

    return render_template(
        "audit_logs.html"
    )


@app.route("/api/audit-logs")
def audit_logs_api():

    conn = get_connection()

    files = conn.execute("""
        SELECT
            filename,
            status,
            risk_level,
            username,
            upload_time
        FROM files
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    events = []

    for f in files:

        events.append({

            "event_type": f["status"],

            "file_name": f["filename"],

            "username": f["username"],

            "risk_level": f["risk_level"],

            "authorization": "AUTHORIZED",

            "event_time": f["upload_time"]

        })

    return jsonify({
        "events": events
    })


@app.route("/reports")
def reports():

    return render_template(
        "report.html"
    )


@app.route("/api/reports")
def reports_api():

    conn = get_connection()

    files = conn.execute("""
        SELECT *
        FROM files
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify({
        "files": [
            dict(f)
            for f in files
        ]
    })


if __name__ == "__main__":

    app.run(debug=True)
