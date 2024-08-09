from flask import Flask 
import urllib3, json, os
import certifi


app = Flask(__name__)



@app.route("/")
def get_movies():
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Glasgow/2024-08-09?key={}'.format(os.environ.get("WEATHER_API_KEY"))
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    try:
        response = http.request('GET', url, timeout=5.0)
        print(response.status)

        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            return (data)
        else:
            print(f"Request failed with status: {response.status}")
    except urllib3.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except urllib3.exceptions.RequestError as e:
        print(f"Request error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return ("<p> arghh! </p>")

@app.get("/<location>")
def get_weather(location):
    pass 



if __name__ == '__main__':
    app.run(debug=True)
