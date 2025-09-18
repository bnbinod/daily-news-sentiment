# Economic/Financial Sentiment Tracker 📈

A real-time economic and financial news sentiment analysis system that automatically fetches, analyzes, and visualizes market sentiment using the Loughran-McDonald financial dictionary.

![Dashboard](https://img.shields.io/badge/Dashboard-Interactive-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-green) ![Flask](https://img.shields.io/badge/Flask-WSGI%20Compatible-lightgrey)

## ✨ Features

- **Automated News Fetching**: Scheduled scraping of financial news from multiple sources
- **Advanced Sentiment Analysis**: Loughran-McDonald financial dictionary for accurate market sentiment
- **Real-time Dashboard**: Interactive Plotly charts with dual Y-axis visualization
- **RESTful API**: Complete API endpoints for data access and integration
- **Database Storage**: SQLite/PostgreSQL persistent storage with SQLAlchemy ORM
- **Background Processing**: Automated scheduled tasks with APScheduler
- **cPanel Compatible**: WSGI configuration for easy deployment on shared hosting

## 🏗 Architecture

```
News APIs → Flask Server → Database → Web Dashboard
    │           │             │            │
    │           │             │            └── Interactive Charts
    │           │             └── SQLAlchemy ORM
    │           └── Background Scheduler
    └── NewsAPI, Reuters, Bloomberg
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- cPanel hosting with Passenger WSGI support
- NewsAPI key (free tier available)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/bnbinod/daily-news-sentiment.git
cd daily-news-sentiment
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Edit .env with your API keys and settings
```

4. **Initialize database (ToDo)**
```bash
python init_db.py
```

### Configuration

Create a `.env` file:

```env
NEWS_API_KEY=your_newsapi_key_here
DATABASE_URL=sqlite:///sentiment.db
UPDATE_INTERVAL_HOURS=6
NEWS_SOURCES=bloomberg,reuters,financial-post
```

## 🌐 Deployment (cPanel)

1. Upload all files to your cPanel public_html directory
2. Ensure `passenger_wsgi.py` is in the root
3. Create Python app through cPanel interface
4. Install requirements via SSH:
```bash
cd ~/public_html/yourdomain.com
pip install -r requirements.txt --user
```

5. Access your dashboard at `https://yourdomain.com`

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard interface |
| `/api/stats` | GET | System statistics and metrics |
| `/api/sentiment-data` | GET | Raw sentiment data (JSON) |
| `/api/dashboard-plot` | GET | Plotly chart configuration |
| `/api/fetch-news` | POST | Manual news fetch trigger |

## 🔧 Usage

### Automated Operation
The system automatically:
- Fetches news every 6 hours (configurable)
- Processes sentiment scores
- Updates the database
- Refreshes dashboard visuals

### Manual Control
- **Dashboard**: Visit your domain to view interactive charts
- **Force Update**: Click "Fetch News Now" button
- **API Access**: Use endpoints for custom integrations

## 📈 Data Model

```python
class SentimentRecord:
    id: Integer
    date: DateTime
    title: String
    summary: Text
    source: String
    url: String
    title_score: Float
    summary_score: Float
    title_positive: Integer
    title_negative: Integer
    # ... and more metrics
```

## 🛠 Customization

### Modify News Sources
Edit `NEWS_SOURCES` in config.py:
```python
NEWS_SOURCES = "bloomberg,reuters,financial-post,cnbc"
```

### Adjust Update Frequency
Change `UPDATE_INTERVAL_HOURS` in config.py:
```python
UPDATE_INTERVAL_HOURS = 4  # Update every 4 hours
```

### Add New Sentiment Metrics
Extend the sentiment analyzer in `sentiment.py`:
```python
def calculate_additional_metrics(self, text):
    # Your custom analysis logic
    pass
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

- [Loughran-McDonald Financial Sentiment Dictionaries](https://sraf.nd.edu/loughranmcdonald-master-dictionary/)
- [NewsAPI](https://newsapi.org/) for news data
- [Plotly](https://plotly.com/) for interactive visualizations
- [Flask](https://flask.palletsprojects.com/) web framework

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the [Wiki](https://github.com/bnbinod/daily-news-sentiment/wiki) for documentation
- Review cPanel [Passenger documentation](https://www.phusionpassenger.com/library/walkthroughs/deploy/python/)

---

**Live Demo**: [https://apps.binod.me/esi](https://apps.binod.me)

*Built with ❤ for financial analysts and data enthusiasts*