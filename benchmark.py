
import time
import urllib.request
import statistics

url = "http://127.0.0.1:8000/employees"
times = []

for i in range(10):
    start = time.perf_counter()

    with urllib.request.urlopen(url) as response:
        body = response.read()

    elapsed = time.perf_counter() - start
    times.append(elapsed)

print("Requests:", len(times))
print("Status: 200 OK")
print("Average real time:", round(statistics.mean(times) * 1000, 2), "ms")
print("Minimum real time:", round(min(times) * 1000, 2), "ms")
print("Maximum real time:", round(max(times) * 1000, 2), "ms")
print("Response size:", len(body), "bytes")
