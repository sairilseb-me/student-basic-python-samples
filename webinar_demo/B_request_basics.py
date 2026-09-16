"""
B - Understanding Requests and Responses
--------------------------------------
Goal: See what actually happens when a frontend (or any client)
"talks to" a backend. Every request has a method and a URL.
Every response has a status code, headers, and usually a JSON body.

Make sure A_api_server.py is already running before this.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"

print("=== GET request: fetch all students ===")
response = requests.get(f"{BASE_URL}/api/students")

print("URL called:", response.url)
print("Status code:", response.status_code)          # 200 = success
print("Content-Type header:", response.headers["Content-Type"])
print("JSON body:", response.json())

print()
print("=== GET request: fetch ONE student ===")
response = requests.get(f"{BASE_URL}/api/students/juan-dela-cruz")
print("Status code:", response.status_code)
print("JSON body:", response.json())

print()
print("=== GET request: a student that does NOT exist ===")
response = requests.get(f"{BASE_URL}/api/students/does-not-exist")
print("Status code:", response.status_code)           # 404 = not found
print("JSON body:", response.json())

print()
print("=== POST request: sign/clear a student ===")
response = requests.post(f"{BASE_URL}/api/students/maria-santos/sign")
print("Status code:", response.status_code)
print("JSON body:", response.json())

print()
print("=== Confirm the change actually happened ===")
response = requests.get(f"{BASE_URL}/api/students/maria-santos")
print("JSON body:", response.json())
