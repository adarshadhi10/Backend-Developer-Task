import requests

FLASK_API = "http://mock-server:5000/api/customers"

def fetch_all_customers():
    page = 1
    limit = 10
    results = []

    while True:
        response = requests.get(f"{FLASK_API}?page={page}&limit={limit}")
        data = response.json()
        results.extend(data["data"])

        if len(results) >= data["total"]:
            break

        page += 1

    return results
