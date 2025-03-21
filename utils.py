import requests
from bs4 import BeautifulSoup
from newspaper import Article
from googlesearch import search

import requests

API_KEY = "ca82e35d47644a6dbac88524f0e2ce85"  # Replace this with your actual key

def get_news_articles(company, num_articles=5):
    """
    Fetches news articles related to the given company from NewsAPI.

    Args:
        company (str): The name of the company to search for.
        num_articles (int): Number of news articles to extract.

    Returns:
        list: A list of dictionaries containing title, summary, and URL.
    """
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={API_KEY}&pageSize={num_articles}"

    response = requests.get(url)
    data = response.json()

    if "articles" not in data or not data["articles"]:
        return []  # No articles found

    news_list = []
    for article in data["articles"]:
        news_list.append({
            "title": article["title"],
            "summary": article["description"] or "No summary available.",
            "url": article["url"]
        })

    return news_list



## Sentiment Analysis
from transformers import pipeline

# Load a sentiment analysis model from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """
    Analyzes sentiment of the given text.

    Args:
        text (str): The input text.

    Returns:
        str: Sentiment category - "Positive", "Negative", or "Neutral".
    """
    result = sentiment_pipeline(text[:512])  # Truncate long text to avoid token limits
    return result[0]["label"]


## Comparative Analysis
from collections import Counter

def comparative_analysis(articles):
    """
    Compares sentiment across multiple articles.

    Args:
        articles (list): List of articles with sentiment analysis results.

    Returns:
        dict: Summary of sentiment distribution.
    """
    sentiments = [article.get("sentiment", "Neutral") for article in articles]
    sentiment_counts = Counter(sentiments)

    return {
        "Positive": sentiment_counts.get("POSITIVE", 0),
        "Negative": sentiment_counts.get("NEGATIVE", 0),
        "Neutral": sentiment_counts.get("NEUTRAL", 0),
    }


## TTS Implementation
# from gtts import gTTS

# def text_to_speech_hindi(text, output_file="output.mp3"):
#     """
#     Converts text into Hindi speech.

#     Args:
#         text (str): Text to be converted to speech.
#         output_file (str): Output file name.

#     Returns:
#         str: Path to the saved audio file.
#     """
#     if not text.strip():
#         return None  # Prevent errors due to empty text
    
#     tts = gTTS(text=text, lang="hi")
#     tts.save(output_file)
#     return output_file

from googletrans import Translator
from gtts import gTTS

def text_to_speech_hindi(text, output_file="output.mp3"):
    translator = Translator()
    translated_text = translator.translate(text, dest="hi").text  # Translate to Hindi
    print("Translated Text:", translated_text)  # Debugging step
    
    tts = gTTS(text=translated_text, lang="hi")
    tts.save(output_file)
    return output_file





