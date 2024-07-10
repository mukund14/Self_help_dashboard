import streamlit as st
import requests
import feedparser
from datetime import datetime, timedelta

# Function to fetch self-help articles from an RSS feed (example)
def fetch_self_help_articles():
    feed_url = 'https://rss.selfhelpzone.com/'  # Replace with a valid self-help RSS feed URL
    feed = feedparser.parse(feed_url)
    
    if feed.bozo:
        st.error("Failed to fetch articles. Please check the RSS feed URL.")
        return []
    
    articles = [(entry.title, entry.link, entry.published) for entry in feed.entries]
    if not articles:
        st.warning("No articles found in the RSS feed.")
    return articles

# Function to filter articles from the last 7 days
def filter_last_7_days(articles):
    today = datetime.today()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    filtered_articles = []

    for article in articles:
        article_date = datetime.strptime(article[2], '%a, %d %b %Y %H:%M:%S %z')
        if article_date.date() in [day.date() for day in last_7_days]:
            filtered_articles.append(article)

    return filtered_articles

# Main function to build the dashboard
def main():
    st.title('Self-Help Dashboard')

    # Fetch self-help articles
    articles = fetch_self_help_articles()
    
    if not articles:
        st.write("No articles available.")
        return
    
    last_7_days_articles = filter_last_7_days(articles)

    # Display data
    st.header('Self-Help Articles - Last 7 Days')
    for article in last_7_days_articles:
        st.write(f"### {article[0]}")
        st.write(f"[Read more]({article[1]})")
        st.write(f"Published on: {article[2]}")
        st.write("---")

if __name__ == '__main__':
    main()
