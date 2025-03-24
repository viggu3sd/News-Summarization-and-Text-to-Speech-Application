import requests

API_KEY = "ca82e35d47644a6dbac88524f0e2ce85"
company = "Tesla"

url = f"https://newsapi.org/v2/everything?q={company}&apiKey={API_KEY}"
response = requests.get(url)

print(f"Status Code: {response.status_code}")
print("Response JSON:", response.json())