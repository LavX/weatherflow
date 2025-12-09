"""Weather Underground data provider."""
import logging
from dataclasses import dataclass
from typing import Optional

import requests

from src.config import config

logger = logging.getLogger(__name__)


@dataclass
class WeatherData:
    """Weather observation data."""
    station_id: int
    temp: float  # °C
    humidity: float  # %
    wind_speed: float  # m/s
    wind_gust: float  # m/s
    wind_dir: float  # degrees
    pressure: float  # Pa
    precip_rate: float  # mm/h
    dewpoint: float  # °C
    uv_index: float


class WeatherUndergroundProvider:
    """Fetch weather data from Weather Underground API."""
    
    def __init__(self):
        self.url = config.get_wu_url()
    
    def fetch(self) -> Optional[WeatherData]:
        """Fetch current weather observations from Weather Underground."""
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            observation = data.get("observations", [None])[0]
            
            if observation is None:
                logger.warning("No observations data found in WU response")
                return None
            
            metric_data = observation.get("metric", {})
            logger.debug("WU Metric Data: %s", metric_data)
            
            return WeatherData(
                station_id=config.WINDY_STATION_ID,
                temp=float(metric_data.get("temp", 0)),
                humidity=float(observation.get("humidity", 0)),
                wind_speed=float(metric_data.get("windSpeed", 0)) / 3.6,  # km/h to m/s
                wind_gust=float(metric_data.get("windGust", 0)) / 3.6,  # km/h to m/s
                wind_dir=float(observation.get("winddir", 0)),
                pressure=float(metric_data.get("pressure", 0)) * 100,  # hPa to Pa
                precip_rate=float(metric_data.get("precipRate", 0)),
                dewpoint=float(metric_data.get("dewpt", 0)),
                uv_index=float(observation.get("uv", 0)),
            )
            
        except requests.RequestException as e:
            logger.error("Failed to fetch data from Weather Underground: %s", e)
            return None
        except (KeyError, TypeError, ValueError) as e:
            logger.error("Error parsing Weather Underground data: %s", e)
            return None