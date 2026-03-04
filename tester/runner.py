import statistics
from datetime import datetime
from storage import insert_run

def run_tests():
    # Exemple : tu remplis latencies selon tes tests
    latencies = [100, 200]  # <-- remplacer par tes données réelles
    passed = 5
    failed = 1
    total = passed + failed
    error_rate = failed / total if total > 0 else 0
    latency_avg = round(sum(latencies)/len(latencies), 2) if latencies else 0
    
    # Calcul du P95 sécurisé
    if len(latencies) >= 2:
        latency_p95 = round(statistics.quantiles(latencies, n=20)[-1], 2)
    else:
        latency_p95 = latencies[0] if latencies else 0

    timestamp = datetime.now().isoformat()
    
    # Sauvegarde dans la base
    insert_run(timestamp, passed, failed, error_rate, latency_avg, latency_p95)

    # Retour pour l'affichage si besoin
    return {
        "timestamp": timestamp,
        "passed": passed,
        "failed": failed,
        "error_rate": error_rate,
        "latency_avg": latency_avg,
        "latency_p95": latency_p95
    }