from flask import Flask, jsonify, render_template
from storage import init_db, list_runs
from tester.runner import run_tests

app = Flask(__name__)

# Initialise la DB au démarrage
init_db()

@app.route('/run')
def run():
    try:
        data = run_tests()
        return jsonify({"status": "ok", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    try:
        runs = list_runs()
        return render_template("dashboard.html", runs=runs)
    except Exception as e:
        return f"Erreur dashboard: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)