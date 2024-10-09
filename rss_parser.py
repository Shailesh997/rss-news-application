import logging
import os
import feedparser
from celery_tasks import classify_and_save

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()  
    ]
)

logger = logging.getLogger(__name__)

feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

def parse_feed(url):
    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            logger.error(f"Failed to parse feed from {url}: {feed.bozo_exception}")
            return []  

        articles = []
        for entry in feed.entries:
            article = {
                'title': entry.title,
                'content': getattr(entry, 'description', None) or getattr(entry, 'summary', None),
                'published_date': entry.published if 'published' in entry else 'No date available',
                'source_url': entry.link
            }
            articles.append(article)
        return articles
    except Exception as e:
        logger.error(f"Error fetching feed from {url}: {e}")
        return []

def remove_duplicates(articles):
    seen = set()
    unique_articles = []
    for article in articles:
        identifier = (article['title'], article['source_url'])  
        if identifier not in seen:
            seen.add(identifier)
            unique_articles.append(article)
    return unique_articles

def process_feeds():
    all_articles = []
    
    for url in feeds:
        logger.info(f"Fetching articles from {url}...")
        try:
            articles = parse_feed(url)
            all_articles.extend(articles)
        except Exception as e:
            logger.error(f"Error fetching articles from {url}: {e}")

    unique_articles = remove_duplicates(all_articles)

    for article in unique_articles:
        logger.info(f"Sending article to Celery for classification: {article['title']}")
        try:
            classify_and_save.delay({
                'title': article['title'],
                'content': article['content'],
                'published_date': article['published_date'],
                'source_url': article['source_url']
            })
        except Exception as e:
            logger.error(f"Error sending article to Celery: {e}")

if __name__ == "__main__":
    process_feeds()
