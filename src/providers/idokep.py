"""Idokep.hu weather data publisher."""
import logging
import re
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
        
        # Handle dewpoint - same 0.0 issue as temperature
        dewpoint = data.dewpoint
        if dewpoint == 0.0:
            dewpoint = 0.1
        
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
            "harmatpont": dewpoint,
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
                # Parse the HTML response to extract the status message
                status_msg = self._parse_response(response.text)
                logger.info("Data successfully sent to Idokep.hu: %s", status_msg)
                return True
            
            logger.error(
                "Failed to send data to Idokep.hu. Status: %d",
                response.status_code
            )
            return False
            
        except requests.RequestException as e:
            logger.error("Error sending data to Idokep.hu: %s", e)
            return False
    
    def _parse_response(self, html: str) -> str:
        """
        Parse the idokep.hu HTML response to extract the status message.
        
        Args:
            html: Raw HTML response from idokep.hu
            
        Returns:
            Extracted status message or 'OK' if parsing fails
        """
        # Try to extract the location and status from the HTML
        # Example: "Beírás ide:<br>Taksony...<br>kész!"
        match = re.search(r"Be[íi]r[áa]s ide:<br>([^<]+)\.\.\.<br>([^<]+)", html)
        if match:
            location = match.group(1).strip()
            status = match.group(2).strip()
            return f"{location} - {status}"
        
        # Check if response contains "kész" (success indicator)
        if "kész" in html.lower():
            return "OK"
        
        return "OK"