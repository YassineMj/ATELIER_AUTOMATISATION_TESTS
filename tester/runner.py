import json
from datetime import datetime
from tester.client import get_with_metrics
from tester import tests
import statistics

API_URL = "https://api.agify.io?name=michael"

def run_tests():
    results = []
    latencies = []

    response, latency, error = get_with_metrics(API_URL)

    if error:
        return {"error": error}

    data = response.json()
    latencies.append(latency)

    test_functions = [
        lambda: tests.test_status_code(response),
        lambda: tests.test_content_type(response),
        lambda: tests.test_name_field(data),
        lambda: tests.test_age_field(data),
        lambda: tests.test_count_field(data),
        tests.test_invalid_param
    ]

    passed = 0

    for t in test_functions:
        ok, msg = t()
        results.append({
            "name": msg,
            "status": "PASS" if ok else "FAIL",
            "latency_ms": latency
        })
        if ok:
            passed += 1

    summary = {
        "timestamp": datetime.now().isoformat(),
        "passed": passed,
        "failed": len(test_functions) - passed,
        "error_rate": round((len(test_functions)-passed)/len(test_functions),3),
        "latency_ms_avg": round(statistics.mean(latencies),2),
        "latency_ms_p95": round(statistics.quantiles(latencies, n=20)[-1],2)
    }

    return {
        "summary": summary,
        "tests": results
    }