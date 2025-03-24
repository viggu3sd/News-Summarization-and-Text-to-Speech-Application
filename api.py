from fastapi import FastAPI, HTTPException
from utils import get_news_articles, analyze_sentiment, comparative_analysis, text_to_speech_hindi

app = FastAPI()

@app.get("/")
def root():
    """
    Root endpoint to indicate the API is running.
    """
    return {"message": "Welcome to the News API! Use /news/?company=CompanyName to fetch news."}

@app.get("/news/")
def get_news(company: str):
    """
    Fetch news articles for a given company, analyze sentiment, 
    perform comparative analysis, and generate text-to-speech.
    
    Parameters:
        company (str): Name of the company to fetch news for.

    Returns:
        dict: Contains company name, articles, sentiment scores, and TTS audio file.
    """
    try:
        articles = get_news_articles(company)
        if not articles:
            raise HTTPException(status_code=404, detail="No news articles found for the given company.")

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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))