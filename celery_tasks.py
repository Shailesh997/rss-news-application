import logging
import os
from celery import Celery
from database import insert_article
from models import Article  
import spacy 

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

app = Celery('rss_tasks', broker='redis://localhost:6379/0')
nlp = spacy.load('en_core_web_sm')  

@app.task
def classify_and_save(article_data):
    try:
        category = classify_article(article_data['content'])
        article_data['category'] = category  
        insert_article(article_data)
        logger.info(f"Successfully inserted article: {article_data['title']}")
    except Exception as e:
        logger.error(f"Error processing article {article_data['title']}: {e}")

def classify_article(content):
    doc = nlp(content)
    categories = {
        'Politics': ['election', 'government', 'policy'],
        'Economy': ['economy', 'market', 'business'],
        'Health': ['health', 'virus', 'vaccine'],
        'Technology': ['technology', 'AI', 'software'],
    }
    for category, keywords in categories.items():
        if any(keyword in doc.text.lower() for keyword in keywords):
            return category

    return 'Uncategorized'  
