import requests
import time

TIMEOUT = 3

def get_with_metrics(url):
    start = time.time()
    try:
        response = requests.get(url, timeout=TIMEOUT)
        latency = round((time.time() - start) * 1000, 2)
        return response, latency, None
    except Exception as e:
        return None, None, str(e)