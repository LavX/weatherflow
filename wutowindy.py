import os
import requests
import time

# Weather Underground API settings
WU_PWS_ID = os.getenv('WU_PWS_ID')
WU_API_KEY = os.getenv('WU_API_KEY')
WU_URL = f"https://api.weather.com/v2/pws/observations/current?stationId={WU_PWS_ID}&format=json&units=m&numericPrecision=decimal&apiKey={WU_API_KEY}"

# Windy API settings
WINDY_API_KEY = os.getenv('WINDY_API_KEY')
WINDY_STATION_ID = int(os.getenv('WINDY_STATION_ID', '0'))
WINDY_URL = f"https://stations.windy.com/pws/update/{WINDY_API_KEY}"

# Configurable update interval (in seconds)
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', '300'))

def fetch_wu_data():
    response = requests.get(WU_URL)
    if response.status_code == 200:
        data = response.json()
        observation = data.get("observations", [None])[0]
        if observation is None:
            print("No observations data found.")
            return None

        # Extract metric data with floating-point precision
        metric_data = observation.get("metric", {})
        print("Metric Data:", metric_data)

        return {
            "stationId": WINDY_STATION_ID,
            "temp": float(metric_data.get("temp")),                  # °C
            "rh": float(observation.get("humidity")),                # %
            "wind": float(metric_data.get("windSpeed")) / 3.6,       # m/s (converted from km/h)
            "gust": float(metric_data.get("windGust")) / 3.6,        # m/s (converted from km/h)
            "winddir": float(observation.get("winddir")),            # Degrees
            "pressure": float(metric_data.get("pressure")) * 100,    # Pa (converted from hPa)
            "precip": float(metric_data.get("precipRate")),          # mm/h
            "dewpoint": float(metric_data.get("dewpt")),             # °C
            "uv": float(observation.get("uv"))                       # UV Index
        }
    else:
        print("Failed to fetch data from Weather Underground.")
        return None

def send_to_windy(data):
    if data:
        payload = {
            "stationId": data.get("stationId"),
            "temp": data.get("temp"),
            "rh": data.get("rh"),
            "wind": data.get("wind"),
            "gust": data.get("gust"),
            "winddir": data.get("winddir"),
            "pressure": data.get("pressure"),
            "precip": data.get("precip"),
            "dewpoint": data.get("dewpoint"),
            "uv": data.get("uv")
        }

        # Sending the request
        response = requests.get(WINDY_URL, params=payload)
        if response.status_code == 200:
            print("Data successfully sent to Windy.")
        else:
            print(f"Failed to send data to Windy. Status code: {response.status_code}")
            print(f"Response content: {response.content}")
    else:
        print("No data to send to Windy.")

def main():
    while True:
        wu_data = fetch_wu_data()
        send_to_windy(wu_data)
        time.sleep(UPDATE_INTERVAL)  # Wait for the configured interval before sending the next update

if __name__ == "__main__":
    main()
