from flask import Flask, render_template, request, redirect
from datetime import datetime
import psycopg2
import os
import locale

app = Flask(__name__)

# =========================
# CONFIG
# =========================
DATABASE_URL = os.environ.get("DATABASE_URL")

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    pass

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# =========================
# LISTAR
# =========================
@app.route("/")
def index():
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT id, task, date, comment FROM tasks")
    rows = c.fetchall()
    conn.close()

    tasks = []

    for row in rows:
        id, task, date, comment = row

        days_left = None
        weekday = ""

        if date:
            try:
                date_obj = datetime.strptime(str(date), "%Y-%m-%d")
                days_left = (date_obj - datetime.now()).days
                weekday = date_obj.strftime("%A")
            except:
                pass

        tasks.append((id, task, date, days_left, weekday, comment))

    # ordenar por data mais próxima
    tasks.sort(key=lambda x: x[2] if x[2] else "9999-12-31")

    return render_template("index.html", tasks=tasks)

# =========================
# ADICIONAR
# =========================
@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    date = request.form["date"]
    comment = request.form["comment"]

    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        INSERT INTO tasks (task, date, comment)
        VALUES (%s, %s, %s)
    """, (task, date, comment))

    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# DELETE
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_conn()
    c = conn.cursor()

    c.execute("DELETE FROM tasks WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return redirect("/")
