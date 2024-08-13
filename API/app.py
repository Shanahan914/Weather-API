from flask import Flask, request, jsonify
import urllib3, json, os
import certifi
import redis 
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

redis_host='redis-14406.c338.eu-west-2-1.ec2.redns.redis-cloud.com'
redis_port=14406
redis_password=os.environ.get("REDIS_PASSWORD")
redis_expiry = 60*60*2  # 2 houes


r = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password)


limiter=Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=f"redis://:{redis_password}@{redis_host}:{redis_port}/0" 
)

@app.get("/<location>")
def get_weather(location):
    filterstart = request.args.get('start', "")
    filterend=request.args.get('end', "")
    redisKey = location + filterstart + filterend

    # try to get data from cache
    try:
        storedData = r.get(redisKey)
        if storedData:
            return jsonify(json.loads(storedData.decode('utf-8')))
    except redis.RedisError as redis_error:
        logging.error(f"Redis error: {redis_error}")
   
   #fetch from api otherwise

    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{filterstart}/{filterend}/?key={os.environ.get("WEATHER_API_KEY")}'
    logging.info(f"Requesting URL: {url}")

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    try:
        response = http.request('GET', url, timeout=5.0)
        if response.status == 200:
            try:
                r.setex(redisKey, time=redis_expiry,value= response.data)
            except redis.RedisError as redis_error:
                logging.error(f"Failed to cache in redis: {redis_error}")

            return json.loads(response.data.decode('utf-8')), 200
        
        else:
            logging.error(f"data return error: {e}")
            return f"Request failed with status: {response.status}", 500
    except urllib3.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
        return f"HTTP error occurred: {e}", 400
    except urllib3.exceptions.RequestError as e:
        logging.error(f"Request error occurred: {e}")
        return(f"Request error occurred: {e}"), 400
    except Exception as e:
        logging.error(f"Other error occurred: {e}")
        return f"An unexpected error occurred: {e}", 500
    return "An error has occurred. Please check whether your request was valid and try again.", 500



if __name__ == '__main__':
    app.run(debug=True)
