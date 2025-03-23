import requests
import time
import subprocess
import gradio as gr

def start_api_server():
    """Starts the FastAPI server using uvicorn."""
    print("\nStarting the API server...\n")
    subprocess.Popen(["uvicorn", "api:app", "--reload"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)  # Give time for the server to start

def is_api_running():
    """Checks if the API is running."""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def fetch_news(company):
    """Fetches news for the given company."""
    if not company.strip():
        return "⚠ Please enter a valid company name."
    
    url = f"http://127.0.0.1:8000/news/?company={company}"

    if not is_api_running():
        start_api_server()

    # Wait for API to be accessible
    for _ in range(5):
        if is_api_running():
            print(f"\nFetching news for: {company}...\n")
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()  # Return the API response as JSON
            return "⚠ No news found or an error occurred."
        time.sleep(2)

    return "⚠ API server is not responding. Please check if `uvicorn` is installed."

# Gradio UI
interface = gr.Interface(
    fn=fetch_news,
    inputs=gr.Textbox(label="🔹 Enter Company Name"),
    outputs=gr.JSON(label="📢 News & Sentiment Analysis"),
    title="📰 News Sentiment Analysis App",
    description="Enter a company name to fetch recent news and analyze sentiment.",
    live=True
)

if __name__ == "__main__":
    interface.launch()
