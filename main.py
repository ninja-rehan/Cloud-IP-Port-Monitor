from fastapi import FastAPI
from fastapi.responses import FileResponse
import sqlite3
import socket
import time
from datetime import datetime

app = FastAPI()


# -----------------------------
# Dashboard
# -----------------------------

@app.get("/dashboard")
def dashboard():
    return FileResponse("index.html")


# -----------------------------
# Database Connection
# -----------------------------

def get_db():
    return sqlite3.connect("monitor.db")


# -----------------------------
# Create Database Table
# -----------------------------

conn = get_db()

conn.execute("""
    CREATE TABLE IF NOT EXISTS targets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        port INTEGER NOT NULL
    )
""")

# Clear targets whenever server starts
conn.execute("DELETE FROM targets")

conn.commit()
conn.close()


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "IP and Port Monitoring System"
    }


# -----------------------------
# Add Target
# -----------------------------

@app.post("/targets")
def add_target(ip: str, port: int):

    conn = get_db()

    conn.execute(
        "INSERT INTO targets (ip, port) VALUES (?, ?)",
        (ip, port)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Target added successfully",
        "ip": ip,
        "port": port
    }


# -----------------------------
# Get Targets
# -----------------------------

@app.get("/targets")
def get_targets():

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM targets"
    ).fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "ip": row[1],
            "port": row[2]
        }
        for row in rows
    ]


# -----------------------------
# Delete Target
# -----------------------------

@app.delete("/targets/{target_id}")
def delete_target(target_id: int):

    conn = get_db()

    conn.execute(
        "DELETE FROM targets WHERE id = ?",
        (target_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Target deleted successfully"
    }


# -----------------------------
# Check IP and Port
# -----------------------------

@app.get("/check")
def check_port(ip: str, port: int):

    start_time = time.time()

    # Create socket
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Timeout
    sock.settimeout(3)

    # Check connection
    result = sock.connect_ex(
        (ip, port)
    )

    # Close socket
    sock.close()

    end_time = time.time()

    # Calculate response time
    response_time = round(
        (end_time - start_time) * 1000,
        2
    )

    # Determine status
    if result == 0:
        status = "OPEN"
    else:
        status = "CLOSED"

    # Current date and time
    checked_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return {
        "ip": ip,
        "port": port,
        "status": status,
        "response_time": response_time,
        "checked_at": checked_at
    }