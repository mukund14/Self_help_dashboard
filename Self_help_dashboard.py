import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Function to fetch self-help articles from a specific website (e.g., Tiny Buddha)
def fetch_self_help_articles():
    url = 'https://tinybuddha.com/blog/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='type-post')

    article_list = []
    for article in articles:
        title = article.find('h2', class_='entry-title').text.strip()
        link = article.find('h2', class_='entry-title').find('a')['href']
        date_published = article.find('time', class_='entry-date').text.strip()
        article_list.append((title, link, date_published))

    return article_list

# Function to filter articles from the last 7 days
def filter_last_7_days(articles):
    today = datetime.today()
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    filtered_articles = []

    for article in articles:
        article_date = datetime.strptime(article[2], '%B %d, %Y')
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
