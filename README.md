# 📚 RSS News Application

## 🚀 Overview
The **RSS News Application** is a Python-based application that fetches news articles from various RSS feeds, classifies them into categories, and stores them in a PostgreSQL database. It utilizes **Celery** for asynchronous processing and **Redis** as a message broker.

---

## 📋 Features
- **Fetch Articles**: Retrieves articles from multiple RSS feeds.
- **Category Classification**: Classifies articles using Natural Language Processing (NLP).
- **Asynchronous Processing**: Uses Celery for handling tasks in the background.
- **Error Logging**: Logs important events and errors for monitoring and debugging.

---

## 🏗️ Architecture
The application is structured as follows:

- **RSS Parser**: 
  - `rss_parser.py` - Responsible for fetching and parsing RSS feeds.
  
- **Celery Tasks**: 
  - `celery_tasks.py` - Handles processing and saving articles to the database.
  
- **Database Management**: 
  - `database.py` - Manages connections and data insertion.
  
- **Data Models**: 
  - `models.py` - Defines the database schema for storing articles.

---

## ⚙️ Installation

### Prerequisites
- Python 3.x
- PostgreSQL
- Redis

### Steps to Set Up
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/rss-news-application.git
