import requests
import time
import statistics

# Configuration
API_URL = "http://localhost:8000/calculate"
PAYLOAD = {
    "year": 1995,
    "month": 8,
    "day": 25,
    "hour": 14,
    "minute": 30,
    "timezone": 5.5,
    "latitude": 28.61,
    "longitude": 77.20,
    "ayanamsa": "LAHIRI",
}
REQUEST_COUNT = 50


def run_benchmark():
    latencies = []
    errors = 0

    print(f"Starting Benchmark: {REQUEST_COUNT} requests to {API_URL}")
    print("-" * 50)

    start_time = time.time()

    for i in range(REQUEST_COUNT):
        t0 = time.time()
        try:
            resp = requests.post(API_URL, json=PAYLOAD)
            if resp.status_code == 200:
                lat = (time.time() - t0) * 1000  # ms
                latencies.append(lat)
                print(f"Request {i + 1}/{REQUEST_COUNT}: {lat:.2f}ms")
            else:
                print(f"Request {i + 1} Failed: {resp.status_code}")
                errors += 1
        except Exception as e:
            print(f"Request {i + 1} Error: {e}")
            errors += 1

    total_time = time.time() - start_time

    if not latencies:
        print("No successful requests.")
        return

    # Calculate statistics
    avg_lat = statistics.mean(latencies)
    median_lat = statistics.median(latencies)
    p95_lat = sorted(latencies)[int(len(latencies) * 0.95)]
    min_lat = min(latencies)
    max_lat = max(latencies)
    throughput = len(latencies) / total_time

    print("\nBENCHMARK RESULTS")
    print("-" * 50)
    print(f"Total Requests: {REQUEST_COUNT}")
    print(f"Successful:     {len(latencies)}")
    print(f"Errors:         {errors}")
    print(f"Throughput:     {throughput:.2f} req/sec")
    print("-" * 50)
    print(f"Min Latency:    {min_lat:.2f} ms")
    print(f"Median Latency: {median_lat:.2f} ms")
    print(f"Ave Latency:    {avg_lat:.2f} ms")
    print(f"P95 Latency:    {p95_lat:.2f} ms")
    print(f"Max Latency:    {max_lat:.2f} ms")
    print("-" * 50)


if __name__ == "__main__":
    run_benchmark()
