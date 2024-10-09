import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Article  

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
DATABASE_URL = "postgresql://rss_user:6853@localhost/rss_news_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

def insert_article(article_data):
    session = get_session()  
    try:
        new_article = Article(
            title=article_data['title'],
            content=article_data['content'],
            published_date=article_data['published_date'],
            source_url=article_data['source_url'],
            category=article_data.get('category')  
        )
        session.add(new_article)
        session.commit()
        logger.info(f"Inserted article: {article_data['title']}")
    except Exception as e:
        logger.error(f"Error inserting article: {e}")
        session.rollback()  
    finally:
        session.close()  
