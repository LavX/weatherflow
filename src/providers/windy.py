"""Windy.com weather data publisher."""
import logging
from typing import Optional

import requests

from src.config import config
from src.providers.weather_underground import WeatherData

logger = logging.getLogger(__name__)


class WindyPublisher:
    """Publish weather data to Windy.com API."""
    
    def __init__(self):
        self.url = config.get_windy_url()
    
    def publish(self, data: Optional[WeatherData]) -> bool:
        """
        Send weather data to Windy.
        
        Args:
            data: Weather observation data
            
        Returns:
            True if successful, False otherwise
        """
        if data is None:
            logger.warning("No data to send to Windy")
            return False
        
        payload = {
            "stationId": data.station_id,
            "temp": data.temp,
            "rh": data.humidity,
            "wind": data.wind_speed,
            "gust": data.wind_gust,
            "winddir": data.wind_dir,
            "pressure": data.pressure,
            "precip": data.precip_rate,
            "dewpoint": data.dewpoint,
            "uv": data.uv_index,
        }
        
        try:
            response = requests.get(self.url, params=payload, timeout=30)
            
            if response.status_code == 200:
                logger.info("Data successfully sent to Windy")
                return True
            
            logger.error(
                "Failed to send data to Windy. Status: %d, Response: %s",
                response.status_code,
                response.text
            )
            return False
            
        except requests.RequestException as e:
            logger.error("Error sending data to Windy: %s", e)
            return False