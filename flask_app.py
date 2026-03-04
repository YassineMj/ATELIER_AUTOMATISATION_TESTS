"""
flask_app.py — Application Web Flask pour le monitoring d'API Agify

Routes :
    /           → redirige vers /dashboard
    /run        → déclenche un run de tests et retourne le JSON
    /dashboard  → tableau de bord visuel (dernier run + historique)
    /health     → health-check du service
    /consignes  → page de consignes de l'atelier (existante)
"""

from flask import Flask, render_template, jsonify, redirect, url_for, request, send_file
import json
import csv
from io import StringIO
from datetime import datetime, timedelta

import storage
from tester import runner

# ── Initialisation de l'application Flask ──
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Création de la base de données au démarrage (idempotent)
storage.init_db()


# ======================================================================
# Route : /  →  redirection vers le dashboard
# ======================================================================
@app.route("/")
def index():
    """Redirige automatiquement l'utilisateur vers le tableau de bord."""
    return redirect(url_for("dashboard"))


# ======================================================================
# Route : /run  →  exécution d'un nouveau run de tests
# ======================================================================
@app.route("/run")
def run_tests():
    """
    Déclenche un run complet des 6 tests via l'orchestrateur,
    puis retourne le résultat en JSON.
    """
    result = runner.execute_run()
    return jsonify(result)


# ======================================================================
# Route : /dashboard  →  tableau de bord visuel
# ======================================================================
@app.route("/dashboard")
def dashboard():
    """
    Récupère l'historique des runs depuis la base SQLite et rend
    le template dashboard.html amélioré avec nouveaux templates.

    Si aucun run n'existe encore, le template recevra `latest=None`
    pour pouvoir afficher un message adapté.
    """
    runs = storage.get_latest_runs(limit=20)

    if not runs:
        # Aucun test n'a encore été lancé
        return render_template("dashboard_enhanced.html", latest=None, history=[])

    # Le premier élément est le run le plus récent (ORDER BY id DESC)
    latest = runs[0]
    history = runs  # on passe tout l'historique (y compris le dernier)

    return render_template("dashboard_enhanced.html", latest=latest, history=history)


# ======================================================================
# Route : /health  →  health-check
# ======================================================================
@app.route("/health")
def health():
    """Retourne un simple indicateur de santé du service."""
    return jsonify({"status": "healthy", "service": "Monitoring API"}), 200


# ======================================================================
# Route : /consignes  →  page de consignes de l'atelier
# ======================================================================
@app.route("/consignes")
def consignes():
    """Affiche la page de consignes HTML."""
    return render_template("consignes.html")


# ======================================================================
# Routes API avancées
# ======================================================================

@app.route("/api/stats")
def api_stats():
    """Retourne les statistiques agrégées de tous les runs."""
    runs = storage.get_latest_runs(limit=100)
    
    if not runs:
        return jsonify({"error": "Aucun run disponible"}), 404
    
    # Calcul des statistiques
    passed_list = [r['passed'] for r in runs]
    failed_list = [r['failed'] for r in runs]
    error_rates = [r['error_rate'] for r in runs]
    latencies_avg = [r['latency_avg'] for r in runs]
    latencies_p95 = [r['latency_p95'] for r in runs]
    
    stats = {
        "total_runs": len(runs),
        "avg_passed": round(sum(passed_list) / len(passed_list), 2),
        "avg_failed": round(sum(failed_list) / len(failed_list), 2),
        "min_error_rate": min(error_rates),
        "max_error_rate": max(error_rates),
        "avg_error_rate": round(sum(error_rates) / len(error_rates), 4),
        "min_latency_avg": min(latencies_avg),
        "max_latency_avg": max(latencies_avg),
        "avg_latency_avg": round(sum(latencies_avg) / len(latencies_avg), 2),
        "min_latency_p95": min(latencies_p95),
        "max_latency_p95": max(latencies_p95),
        "avg_latency_p95": round(sum(latencies_p95) / len(latencies_p95), 2),
    }
    return jsonify(stats)


@app.route("/api/runs")
def api_runs():
    """Retourne les données JSON des runs pour les graphiques."""
    limit = request.args.get('limit', 50, type=int)
    runs = storage.get_latest_runs(limit=limit)
    
    # Inverser pour avoir l'ordre chronologique
    runs_reversed = list(reversed(runs))
    
    return jsonify({
        "runs": runs_reversed,
        "count": len(runs_reversed)
    })


@app.route("/api/compare/<int:run1_id>/<int:run2_id>")
def api_compare(run1_id, run2_id):
    """Compare deux runs spécifiques."""
    all_runs = storage.get_latest_runs(limit=200)
    
    run1 = next((r for r in all_runs if r['id'] == run1_id), None)
    run2 = next((r for r in all_runs if r['id'] == run2_id), None)
    
    if not run1 or not run2:
        return jsonify({"error": "Run non trouvé"}), 404
    
    comparison = {
        "run1": run1,
        "run2": run2,
        "differences": {
            "passed_delta": run2['passed'] - run1['passed'],
            "failed_delta": run2['failed'] - run1['failed'],
            "error_rate_delta": round(run2['error_rate'] - run1['error_rate'], 4),
            "latency_avg_delta": round(run2['latency_avg'] - run1['latency_avg'], 2),
            "latency_p95_delta": round(run2['latency_p95'] - run1['latency_p95'], 2),
        }
    }
    return jsonify(comparison)


@app.route("/export/csv")
def export_csv():
    """Exporte les runs en CSV."""
    runs = storage.get_latest_runs(limit=200)
    
    if not runs:
        return jsonify({"error": "Aucun run à exporter"}), 404
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Timestamp', 'Passed', 'Failed', 'Error Rate', 'Latency Avg (ms)', 'Latency P95 (ms)'])
    
    # Data
    for r in reversed(runs):
        writer.writerow([
            r['id'],
            r['timestamp'],
            r['passed'],
            r['failed'],
            r['error_rate'],
            r['latency_avg'],
            r['latency_p95']
        ])
    
    response_text = output.getvalue()
    output.close()
    
    return response_text, 200, {
        'Content-Disposition': f"attachment; filename=agify_monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        'Content-Type': 'text/csv'
    }


@app.route("/export/json")
def export_json():
    """Exporte les runs en JSON."""
    runs = storage.get_latest_runs(limit=200)
    
    if not runs:
        return jsonify({"error": "Aucun run à exporter"}), 404
    
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "total_runs": len(runs),
        "runs": list(reversed(runs))
    }
    
    return jsonify(export_data)


@app.route("/api/alerts")
def api_alerts():
    """Vérifie les seuils QoS et retourne les alertes actives."""
    runs = storage.get_latest_runs(limit=10)
    
    if not runs:
        return jsonify({"alerts": []})
    
    latest = runs[0]
    alerts = []
    
    # Seuils configurables
    thresholds = {
        "error_rate_critical": 0.5,  # > 50%
        "error_rate_warning": 0.2,   # > 20%
        "latency_critical": 5000,    # > 5000ms
        "latency_warning": 2000,     # > 2000ms
        "failed_tests_critical": 3   # 3+ tests failed
    }
    
    # Vérifier les seuils
    if latest['error_rate'] > thresholds['error_rate_critical']:
        alerts.append({
            "level": "critical",
            "message": f"Taux d'erreur critique: {(latest['error_rate']*100):.1f}%",
            "value": latest['error_rate']
        })
    elif latest['error_rate'] > thresholds['error_rate_warning']:
        alerts.append({
            "level": "warning",
            "message": f"Taux d'erreur élevé: {(latest['error_rate']*100):.1f}%",
            "value": latest['error_rate']
        })
    
    if latest['latency_avg'] > thresholds['latency_critical']:
        alerts.append({
            "level": "critical",
            "message": f"Latence critique: {latest['latency_avg']}ms",
            "value": latest['latency_avg']
        })
    elif latest['latency_avg'] > thresholds['latency_warning']:
        alerts.append({
            "level": "warning",
            "message": f"Latence élevée: {latest['latency_avg']}ms",
            "value": latest['latency_avg']
        })
    
    if latest['failed'] >= thresholds['failed_tests_critical']:
        alerts.append({
            "level": "critical",
            "message": f"{latest['failed']} tests échoués",
            "value": latest['failed']
        })
    
    return jsonify({
        "alerts": alerts,
        "has_critical": any(a['level'] == 'critical' for a in alerts),
        "run_id": latest['id'],
        "timestamp": latest['timestamp']
    })


# ======================================================================
# Point d'entrée
# ======================================================================

@app.route("/api/docs")
def api_docs():
    """Documentation des endpoints API disponibles."""
    docs = {
        "service": "Monitoring API Agify",
        "version": "2.0",
        "endpoints": {
            "GET /": "Redirection vers le dashboard",
            "GET /dashboard": "Tableau de bord avec graphiques et historique",
            "GET /health": "Health Check du service",
            "GET /run": "Déclenche un nouveau run de tests",
            "GET /api/stats": "Statistiques agrégées de tous les runs",
            "GET /api/runs?limit=50": "Liste des runs en JSON (limit: 10-100)",
            "GET /api/compare/<run1>/<run2>": "Compare deux runs spécifiques",
            "GET /api/alerts": "Vérifie les seuils QoS et retourne les alertes",
            "GET /api/performance": "Performance metrics par test",
            "GET /export/csv": "Exporte l'historique en CSV",
            "GET /export/json": "Exporte l'historique en JSON",
            "GET /consignes": "Page de consignes de l'atelier"
        },
        "features": [
            "Graphiques interactifs avec Chart.js",
            "Mode sombre automatique",
            "Auto-refresh configurable",
            "Alertes basées sur les seuils QoS",
            "Export des données (CSV, JSON)",
            "Comparaison entre runs",
            "Statistiques avancées"
        ]
    }
    return jsonify(docs)


@app.route("/analytics")
def analytics():
    """Page d'analytique avancée."""
    return render_template("analytics.html")


@app.route("/settings")
def settings():
    """Page de configuration."""
    return render_template("settings.html")


@app.route("/testlogs")
def testlogs():
    """Page de détail des tests."""
    return render_template("testlogs.html")


@app.route("/api/performance")
def api_performance():
    """Retourne les metrics de performance par test."""
    runs = storage.get_latest_runs(limit=100)
    
    if not runs:
        return jsonify({"error": "Aucun run disponible"}), 404
    
    # Agrégation par test
    test_metrics = {}
    
    for run in runs:
        raw_json = run.get('raw_tests_json', {})
        if isinstance(raw_json, str):
            raw_json = json.loads(raw_json)
        
        tests = raw_json.get('tests', [])
        for test in tests:
            name = test.get('name', 'unknown')
            if name not in test_metrics:
                test_metrics[name] = {
                    'name': name,
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'latencies': []
                }
            
            test_metrics[name]['total'] += 1
            if test['status'] == 'PASS':
                test_metrics[name]['passed'] += 1
            else:
                test_metrics[name]['failed'] += 1
            
            if test.get('latency_ms'):
                test_metrics[name]['latencies'].append(test['latency_ms'])
    
    # Calcul des stats finales
    tests_data = []
    for name, metrics in test_metrics.items():
        avg_latency = sum(metrics['latencies']) / len(metrics['latencies']) if metrics['latencies'] else 0
        success_rate = (metrics['passed'] / metrics['total'] * 100) if metrics['total'] > 0 else 0
        
        tests_data.append({
            'name': name,
            'total_runs': metrics['total'],
            'success_count': metrics['passed'],
            'fail_count': metrics['failed'],
            'success_rate': round(success_rate, 1),
            'avg_latency': round(avg_latency, 2),
            'min_latency': min(metrics['latencies']) if metrics['latencies'] else 0,
            'max_latency': max(metrics['latencies']) if metrics['latencies'] else 0
        })
    
    return jsonify({
        "total_tests": len(tests_data),
        "tests": tests_data
    })


@app.route("/api/clear-old-data", methods=['POST'])
def api_clear_old_data():
    """Nettoie les données de plus de 30 jours."""
    deleted = storage.clear_old_runs(days=30)
    return jsonify({"deleted": deleted})


@app.route("/api/export-db")
def api_export_db():
    """Exporte la base de données."""
    from pathlib import Path
    db_file = Path(__file__).parent / "monitoring.db"
    
    if db_file.exists():
        return send_file(
            str(db_file),
            as_attachment=True,
            download_name=f"monitoring_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )
    return jsonify({"error": "Database not found"}), 404


@app.route("/api/test-alerts", methods=['POST'])
def api_test_alerts():
    """Envoie une alerte de test."""
    alert_data = {
        "type": "test_alert",
        "message": "Ceci est une alerte de test",
        "timestamp": datetime.now().isoformat(),
        "severity": "info"
    }
    return jsonify(alert_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
