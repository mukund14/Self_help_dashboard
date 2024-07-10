import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Function to fetch self-help articles from the web
def fetch_self_help_articles():
    query = "self-help"
    url = f"https://www.google.com/search?q=query"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    for item in soup.find_all('div', class_='dbsr'):
        title = item.find('div', class_='JheGif nDgy9d').text
        link = item.find('a')['href']
        snippet = item.find('div', class_='Y3v8qd').text
        date_published = item.find('span', class_='WG9SHc').find('span').text
        articles.append((title, link, snippet, date_published))
    
    return articles

# Function to filter articles from the last 7 days
def filter_last_7_days(articles):
    today = datetime.today()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    filtered_articles = []

    for article in articles:
        article_date_str = article[3]
        try:
            # Parse the date
            article_date = datetime.strptime(article_date_str, '%b %d, %Y')
        except ValueError:
            continue
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
        st.write(f"{article[2]}")
        st.write(f"Published on: {article[3]}")
        st.write("---")

if __name__ == '__main__':
    main()
