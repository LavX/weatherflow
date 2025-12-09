import os
import requests
import time
from datetime import datetime

# Weather Underground API settings
WU_PWS_ID = os.getenv('WU_PWS_ID')
WU_API_KEY = os.getenv('WU_API_KEY')
WU_URL = f"https://api.weather.com/v2/pws/observations/current?stationId={WU_PWS_ID}&format=json&units=m&numericPrecision=decimal&apiKey={WU_API_KEY}"

# Windy API settings
WINDY_API_KEY = os.getenv('WINDY_API_KEY')
WINDY_STATION_ID = int(os.getenv('WINDY_STATION_ID', '0'))
WINDY_URL = f"https://stations.windy.com/pws/update/{WINDY_API_KEY}"

# Idokep.hu API settings
IDOKEP_ENABLED = os.getenv('IDOKEP_ENABLED', 'false').lower() == 'true'
IDOKEP_USER = os.getenv('IDOKEP_USER', '')
IDOKEP_PASS = os.getenv('IDOKEP_PASS', '')
IDOKEP_STATION_TYPE = os.getenv('IDOKEP_STATION_TYPE', 'PWS')
IDOKEP_PRO = os.getenv('IDOKEP_PRO', 'false').lower() == 'true'
IDOKEP_UTC = int(os.getenv('IDOKEP_UTC', '1'))  # 0=Central European local time, 1=UTC
IDOKEP_URL = "https://pro.idokep.hu/sendws.php" if IDOKEP_PRO else "https://automata.idokep.hu/sendws.php"

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


def send_to_idokep(data):
    """Send weather data to idokep.hu API."""
    if not IDOKEP_ENABLED:
        return
    
    if not IDOKEP_USER or not IDOKEP_PASS:
        print("Idokep.hu credentials not configured. Skipping.")
        return
    
    if not data:
        print("No data to send to Idokep.hu.")
        return
    
    # Get current time based on IDOKEP_UTC setting
    if IDOKEP_UTC == 1:
        now = datetime.utcnow()
    else:
        now = datetime.now()  # Local time (Central European)
    
    # Handle temperature - idokep.hu doesn't accept 0.0, must use 0.1
    temp = data.get("temp")
    if temp is not None and temp == 0.0:
        temp = 0.1
    
    # Build the payload
    payload = {
        "user": IDOKEP_USER,
        "pass": IDOKEP_PASS,
        "utc": IDOKEP_UTC,
        "ev": now.year,
        "honap": now.month,
        "nap": now.day,
        "ora": now.hour,
        "perc": now.minute,
        "mp": now.second,
        "tipus": IDOKEP_STATION_TYPE,
    }
    
    # Add optional parameters only if they have values
    if temp is not None:
        payload["hom"] = temp
    
    if data.get("rh") is not None:
        payload["rh"] = data.get("rh")
    
    if data.get("winddir") is not None:
        payload["szelirany"] = int(data.get("winddir"))
    
    if data.get("wind") is not None:
        payload["szelero"] = round(data.get("wind"), 1)
    
    if data.get("gust") is not None:
        payload["szellokes"] = round(data.get("gust"), 1)
    
    # Pressure - convert from Pa back to hPa for sea level pressure
    if data.get("pressure") is not None:
        payload["p"] = round(data.get("pressure") / 100, 1)
    
    if data.get("uv") is not None:
        payload["uv"] = data.get("uv")
    
    # Precipitation rate as 1-hour precipitation approximation
    if data.get("precip") is not None:
        payload["csap1h"] = round(data.get("precip"), 1)
    
    print(f"Idokep.hu payload: {payload}")
    
    # Send the request
    try:
        response = requests.get(IDOKEP_URL, params=payload)
        if response.status_code == 200:
            print(f"Data successfully sent to Idokep.hu. Response: {response.text}")
        else:
            print(f"Failed to send data to Idokep.hu. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending data to Idokep.hu: {e}")


def main():
    while True:
        wu_data = fetch_wu_data()
        send_to_windy(wu_data)
        send_to_idokep(wu_data)
        time.sleep(UPDATE_INTERVAL)  # Wait for the configured interval before sending the next update


if __name__ == "__main__":
    main()
