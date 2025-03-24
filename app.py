import requests
import webbrowser
import time  # To give time for the server to start

def fetch_news(company):
    url = f"http://127.0.0.1:8000/news/?company={company}"
    time.sleep(2)  # Give server time to start
    webbrowser.open(url)  # Open the API link in a browser
    return url

if __name__ == "__main__":
    interface.launch()
