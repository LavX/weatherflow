"""Idokep.hu weather data publisher."""
import logging
from datetime import datetime, timezone
from typing import Optional

import requests

from src.config import config
from src.providers.weather_underground import WeatherData

logger = logging.getLogger(__name__)


class IdokepPublisher:
    """Publish weather data to idokep.hu API."""
    
    def __init__(self):
        self.url = config.get_idokep_url()
        self.enabled = config.IDOKEP_ENABLED
    
    def publish(self, data: Optional[WeatherData]) -> bool:
        """
        Send weather data to idokep.hu.
        
        Args:
            data: Weather observation data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return True  # Not an error if disabled
        
        if not config.IDOKEP_USER or not config.IDOKEP_PASS:
            logger.warning("Idokep.hu credentials not configured. Skipping.")
            return False
        
        if data is None:
            logger.warning("No data to send to Idokep.hu")
            return False
        
        # Get current time based on UTC setting
        if config.IDOKEP_UTC == 1:
            now = datetime.now(timezone.utc)
        else:
            now = datetime.now()  # Local time (Central European)
        
        # Handle temperature - idokep.hu doesn't accept 0.0, must use 0.1
        temp = data.temp
        if temp == 0.0:
            temp = 0.1
        
        payload = {
            "user": config.IDOKEP_USER,
            "pass": config.IDOKEP_PASS,
            "utc": config.IDOKEP_UTC,
            "ev": now.year,
            "honap": now.month,
            "nap": now.day,
            "ora": now.hour,
            "perc": now.minute,
            "mp": now.second,
            "tipus": config.IDOKEP_STATION_TYPE,
            "hom": temp,
            "rh": data.humidity,
            "szelirany": int(data.wind_dir),
            "szelero": round(data.wind_speed, 1),
            "szellokes": round(data.wind_gust, 1),
            "p": round(data.pressure / 100, 1),  # Pa to hPa
            "uv": data.uv_index,
            "csap1h": round(data.precip_rate, 1),
        }
        
        logger.debug("Idokep.hu payload: %s", payload)
        
        try:
            response = requests.get(self.url, params=payload, timeout=30)
            
            if response.status_code == 200:
                logger.info("Data successfully sent to Idokep.hu. Response: %s", response.text)
                return True
            
            logger.error(
                "Failed to send data to Idokep.hu. Status: %d, Response: %s",
                response.status_code,
                response.text
            )
            return False
            
        except requests.RequestException as e:
            logger.error("Error sending data to Idokep.hu: %s", e)
            return False