from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

# =========================
# BANCO DE DADOS
# =========================
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            date TEXT,
            days_left INTEGER,
            comment TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =========================
# LISTAR TAREFAS
# =========================
@app.route("/")
def index():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT id, task, date, days_left, comment FROM tasks")
    tasks = c.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

# =========================
# ADICIONAR TAREFA
# =========================
@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    date_str = request.form["date"]
    comment = request.form["comment"]

    days_left = None

    if date_str:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            days_left = (date - datetime.now()).days
        except:
            pass

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO tasks (task, date, days_left, comment)
        VALUES (?, ?, ?, ?)
    """, (task, date_str, days_left, comment))
    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# DELETAR TAREFA
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# RODAR APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
