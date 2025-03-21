from fastapi import FastAPI # type: ignore
from utils import get_news_articles, analyze_sentiment, comparative_analysis, text_to_speech_hindi

app = FastAPI()

@app.get("/news/")
def get_news(company: str):
    articles = get_news_articles(company)
    for article in articles:
        article["sentiment"] = analyze_sentiment(article["summary"])
    
    sentiment_summary = comparative_analysis(articles)
    tts_file = text_to_speech_hindi(" ".join([article["summary"] for article in articles]))

    return {
        "Company": company,
        "Articles": articles,
        "Comparative Sentiment Score": sentiment_summary,
        "Audio": tts_file
    }

