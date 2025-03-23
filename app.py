import os
import time
import requests
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
from gtts import gTTS
import psutil

# 🔹 Kill any existing process on port 8000
def kill_existing_processes(port=8000):
    for proc in psutil.process_iter(attrs=["pid", "connections"]):
        try:
            for conn in proc.info["connections"]:
                if conn.laddr.port == port:
                    print(f"Killing process {proc.info['pid']} using port {port}")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

kill_existing_processes(8000)  # Clean port before running FastAPI

app = FastAPI()

# 🔹 Allow CORS for Gradio UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "✅ API is running!"}

@app.get("/news/")
def fetch_news(company: str):
    """Fetch mock news and generate speech."""
    if not company.strip():
        return {"error": "⚠ Please enter a valid company name."}
    
    news = [
        {"headline": f"Breaking news about {company}!", "sentiment": "Positive"},
        {"headline": f"{company} stock surges!", "sentiment": "Neutral"},
    ]
    
    # Convert headlines to speech
    headlines_text = ". ".join([item["headline"] for item in news])
    tts = gTTS(text=headlines_text, lang="en")
    audio_path = os.path.abspath("output.mp3")  # 🔹 Use full file path
    tts.save(audio_path)

    return {
        "company": company,
        "news": news,
        "audio": audio_path  # 🔹 Ensure full file path is sent
    }

# 🔹 Function to start FastAPI in a separate thread
def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# 🔹 Function to call FastAPI from Gradio UI
def gradio_fetch_news(company):
    """Calls FastAPI to fetch news and generates TTS output."""
    url = f"http://127.0.0.1:8000/news/?company={company}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                return data["error"], None  # Handle errors
            
            # 🔹 Ensure 'audio' key exists and return proper path
            audio_file = data.get("audio", None)
            if audio_file and os.path.exists(audio_file):
                return data, audio_file
            else:
                return data, None  # Return news without audio if missing
            
        return {"error": "⚠ No news found or an error occurred."}, None
    except requests.exceptions.ConnectionError:
        return {"error": "⚠ API server is not responding."}, None

# 🔹 Start FastAPI in a background thread
threading.Thread(target=start_fastapi, daemon=True).start()

# 🔹 Gradio UI with Audio Output
interface = gr.Interface(
    fn=gradio_fetch_news,
    inputs=gr.Textbox(label="🔹 Enter Company Name"),
    outputs=[gr.JSON(label="📢 News & Sentiment Analysis"), gr.Audio(label="🔊 Listen to News")],
    title="📰 News Sentiment Analysis App",
    description="Enter a company name to fetch recent news and analyze sentiment.",
    live=True
)

if __name__ == "__main__":
    interface.launch()
