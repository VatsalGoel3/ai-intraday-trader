from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(headline: str) -> dict:
    """
    Analyzes the sentiment of a news headline using two methods:
    Hugging Face Transformers and VADER.

    Parameters:
        headline (str): The news headline to analyze.

    Returns:
        dict: Combined sentiment results from both methods.
    """
    # Hugging Face sentiment-analysis pipeline
    hf_pipeline = pipeline("sentiment-analysis")
    hf_result = hf_pipeline(headline)[0]

    # VADER sentiment Analyzer
    vader_analyzer = SentimentIntensityAnalyzer()
    vader_result = vader_analyzer.polarity_scores(headline)

    combined_result = {
        "hf_label": hf_result['label'],             # Hugging Face label (e.g., +ve or -ve)
        "hf_score": hf_result['score'],              # Hugging Face confidence score
        "vader_compound": vader_result['compound'], # VADER compound sentiment score
        "vader_pos": vader_result['pos'],           # +ve sentiment ratio
        "vader_neu": vader_result['neu'],           # Neutral sentiment ratio
        "vader_neg": vader_result['neg']            # -ve sentiment ratio
    }

    return combined_result

if __name__ == "__main__":
    # Example
    headline = "EUR/USD surges as market sentiment improves amid positive economic news."
    sentiment = analyze_sentiment(headline)
    print("Sentiment Analysis:", sentiment)