import gradio as gr
import requests

def fetch_news(company):
    response = requests.get(f"http://127.0.0.1:8000/news/?company={company}")
    if response.status_code == 200:
        return response.json()
    return "Error fetching data."

interface = gr.Interface(
    fn=fetch_news,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=gr.JSON(),
    title="News Sentiment Analysis",
)

interface.launch()

