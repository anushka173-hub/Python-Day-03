
import json
import time
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"
DEPARTMENT_ID = 1

def request_json(url, method="GET", data=None):
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(
        url, data=body, headers=headers, method=method
    )

    with urllib.request.urlopen(req) as response:
        raw = response.read()
        return json.loads(raw) if raw else None

try:
    employees = request_json(f"{BASE_URL}/employees?limit=100")
    current_count = len(employees)

    if current_count >= 100:
        print(f"Already have {current_count} employees. Nothing to add.")
    else:
        needed = 100 - current_count
        unique_prefix = time.time_ns()

        for i in range(needed):
            number = i + 1
            payload = {
                "name": f"Test Employee {number}",
                "email": f"pagination_{unique_prefix}_{number}@example.com",
                "salary": 50000,
                "department_id": DEPARTMENT_ID,
                "status": "ACTIVE"
            }

            request_json(
                f"{BASE_URL}/employees",
                method="POST",
                data=payload
            )

        employees = request_json(f"{BASE_URL}/employees?limit=100")
        print(f"Employees now in database: {len(employees)}")

except urllib.error.HTTPError as e:
    print("HTTP error:", e.code)
    print(e.read().decode("utf-8"))
except urllib.error.URLError as e:
    print("Could not connect to FastAPI:", e.reason)
