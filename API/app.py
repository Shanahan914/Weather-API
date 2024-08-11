from flask import Flask, request
import urllib3, json, os
import certifi
import redis 


app = Flask(__name__)


@app.get("/<location>")
def get_weather(location):
    print(location)
    filterstartarg = request.args.get('start')
    filterendarg=request.args.get('end')
    filterstart = filterstartarg if filterstartarg else ""
    filterend = filterendarg if filterendarg else ""
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start}/{end}/?key={key}'.format(key=os.environ.get("WEATHER_API_KEY"), location=location, start=filterstart, end=filterend)

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
    return "An error has occurred"



if __name__ == '__main__':
    app.run(debug=True)
