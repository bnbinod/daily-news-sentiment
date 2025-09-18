from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_executor import Executor
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
import threading
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///./instance/sentiment.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home2/binodme/public_html/apps.binod.me/sentiment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
executor = Executor(app)


# Database Model
class SentimentRecord(db.Model):
    __tablename__ = "sentiment_records"

    id = db.Column(db.Integer, primary_key=True, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    title = db.Column(db.String(500))
    summary = db.Column(db.Text)
    source = db.Column(db.String(100))
    url = db.Column(db.String(500))
    title_score = db.Column(db.Float)
    summary_score = db.Column(db.Float)
    title_positive = db.Column(db.Integer)
    title_negative = db.Column(db.Integer)
    summary_positive = db.Column(db.Integer)
    summary_negative = db.Column(db.Integer)


# Initialize database
with app.app_context():
    db.create_all()

# Import your existing modules
from news_fetcher import NewsFetcher, analyzer

news_fetcher = NewsFetcher()

# Scheduler for background tasks
scheduler = BackgroundScheduler()


def background_fetch_news():
    """Background task to fetch and process news"""
    with app.app_context():
        try:
            count = news_fetcher.process_news(db)
            print(f"Processed {count} new articles at {datetime.now()}")
        except Exception as e:
            print(f"Error in background fetch: {e}")


# Configure scheduler
scheduler.add_job(
    func=background_fetch_news,
    trigger='interval',
    hours=6,
    next_run_time=datetime.now()  # Run immediately on startup
)

# This is disabled by Binod
# as the fetch mechanism is yet to be deployed.
# scheduler.start()


@app.route('/')
def index():
    """Serve the dashboard"""
    with open('static/index.html') as f:
        return f.read()


@app.route('/api/fetch-news', methods=['POST'])
def fetch_news():
    """Trigger news fetch manually"""
    executor.submit(background_fetch_news)
    return jsonify({"message": "News fetch started in background"})


@app.route('/api/sentiment-data')
def get_sentiment_data():
    """Get sentiment data for visualization"""
    days = int(request.args.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)

    records = SentimentRecord.query.filter(
        SentimentRecord.date >= start_date
    ).all()

    if not records:
        return jsonify({"error": "No data available"})

    # Convert to DataFrame for processing
    df = pd.DataFrame([{
        'date': r.date,
        'title_score': r.title_score,
        'summary_score': r.summary_score,
        'source': r.source
    } for r in records])

    # Daily aggregation
    df['date_only'] = df['date'].dt.date
    daily_df = df.groupby('date_only').agg({
        'title_score': 'mean',
        'summary_score': 'mean'
    }).reset_index()

    # Count articles per day
    article_count = df.groupby('date_only').size().reset_index(name='article_count')
    daily_df = daily_df.merge(article_count, on='date_only')

    return jsonify(daily_df.to_dict('records'))


@app.route('/api/dashboard-plot')
def get_dashboard_plot():
    """Generate Plotly dashboard"""
    days = int(request.args.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)

    records = SentimentRecord.query.filter(
        SentimentRecord.date >= start_date
    ).all()

    if not records:
        return jsonify({"error": "No data available"})

    df = pd.DataFrame([{
        'date': r.date,
        'title_score': r.title_score,
        'summary_score': r.summary_score
    } for r in records])

    df['date_only'] = df['date'].dt.date
    daily_df = df.groupby('date_only').agg({
        'title_score': 'mean',
        'summary_score': 'mean'
    }).reset_index()

    article_count = df.groupby('date_only').size().reset_index(name='article_count')
    daily_df = daily_df.merge(article_count, on='date_only')

    # Create plot
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=daily_df['date_only'], y=daily_df['title_score'],
                   name="Title Score", line=dict(color='red')),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=daily_df['date_only'], y=daily_df['summary_score'],
                   name="Summary Score", line=dict(color='blue')),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(x=daily_df['date_only'], y=daily_df['article_count'],
               name="Article Count", marker_color='rgba(0, 255, 0, 0.4)'),
        secondary_y=True,
    )

    fig.update_layout(
        title="Financial Sentiment Dashboard",
        xaxis_title="Date",
        yaxis_title="Sentiment Score",
        yaxis2=dict(title="Article Count", overlaying="y", side="right"),
        hovermode='x unified'
    )

    return json.loads(fig.to_json())


@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    total_articles = SentimentRecord.query.count()
    latest_article = SentimentRecord.query.order_by(SentimentRecord.date.desc()).first()
    avg_title = db.session.query(db.func.avg(SentimentRecord.title_score)).scalar()
    avg_summary = db.session.query(db.func.avg(SentimentRecord.summary_score)).scalar()

    return jsonify({
        "total_articles": total_articles,
        "latest_update": latest_article.date.isoformat() if latest_article else None,
        "average_title_score": round(avg_title, 3) if avg_title else None,
        "average_summary_score": round(avg_summary, 3) if avg_summary else None
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
