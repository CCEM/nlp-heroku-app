"""Funcionality to analyze sentiment."""
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def evaluate_comments(comment_text):
    """Returns rating on comment text for sentiment."""
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(comment_text)
    return score['compound']
