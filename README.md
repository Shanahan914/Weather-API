# Weather API with Flask, Redis, and Flask-Limiter

This project is a Flask-based web application that fetches weather data for a given location from the Visual Crossing Weather API. The application implements caching using Redis and rate limiting using Flask-Limiter.

## Features

- **Weather Data Fetching**: Retrieves weather data for a specified location using the Visual Crossing Weather API.
- **Caching with Redis**: Caches the weather data in Redis to reduce API calls and improve performance.
- **Rate Limiting with Flask-Limiter**: Limits the number of API requests a user can make to prevent abuse.

## Requirements

- Python 3.x
- Flask
- Redis (Cloud or local instance)
- Visual Crossing Weather API Key
- SSL/TLS support for Redis connections

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```
###2. Install dependencies 
```
pip install -r requirements.txt
```
###3. Environment variables
```
touch.env
REDIS_PASSWORD=your_redis_password
WEATHER_API_KEY=your_visual_crossing_weather_api_key
```

###4. Run the application
```
python app.py
```
 which will run on port 500 as default.
