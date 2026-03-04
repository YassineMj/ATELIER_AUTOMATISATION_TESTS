from flask import Flask, render_template, jsonify
from tester.runner import run_tests
from storage import init_db, save_run, list_runs

app = Flask(__name__)
init_db()

@app.get("/")
def consignes():
    return render_template("consignes.html")

@app.get("/run")
def run():
    data = run_tests()
    save_run(data)
    return jsonify(data)

@app.get("/dashboard")
def dashboard():
    runs = list_runs()
    return render_template("dashboard.html", runs=runs)

@app.get("/health")
def health():
    return {"status":"ok"}