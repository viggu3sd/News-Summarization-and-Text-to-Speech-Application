import requests
from bs4 import BeautifulSoup
from newspaper import Article

def get_news_articles(company, num_articles=10):
    """
    Extracts news articles related to the given company.

    Args:
        company (str): The name of the company to search for.
        num_articles (int): Number of news articles to extract.

    Returns:
        list: A list of dictionaries containing title, summary, and URL.
    """
    search_url = f"https://news.google.com/search?q={company}&hl=en"
    headers = {"User-Agent": "Mozilla/5.0"}  # Required to avoid blocking by Google
    
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", {"class": "DY5T1d"}, limit=num_articles)
    
    news_list = []
    for article in articles:
        link = "https://news.google.com" + article['href'][1:]  # Fix relative links
        news_article = Article(link)
        news_article.download()
        news_article.parse()
        news_article.nlp()  # Generate a summary

        news_list.append({
            "title": news_article.title,
            "summary": news_article.summary,
            "url": link
        })
    
    return news_list

##Sentiment Analysis
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


##comparitive analysis
from collections import Counter

def comparative_analysis(articles):
    """
    Compares sentiment across multiple articles.

    Args:
        articles (list): List of articles with sentiment analysis results.

    Returns:
        dict: Summary of sentiment distribution.
    """
    sentiments = [article["sentiment"] for article in articles]
    sentiment_counts = Counter(sentiments)

    return {
        "Positive": sentiment_counts.get("POSITIVE", 0),
        "Negative": sentiment_counts.get("NEGATIVE", 0),
        "Neutral": sentiment_counts.get("NEUTRAL", 0),
    }

##TTS Implementation
from gtts import gTTS

def text_to_speech_hindi(text, output_file="output.mp3"):
    """
    Converts text into Hindi speech.

    Args:
        text (str): Text to be converted to speech.
        output_file (str): Output file name.

    Returns:
        str: Path to the saved audio file.
    """
    tts = gTTS(text=text, lang="hi")
    tts.save(output_file)
    return output_file
