"""WeatherFlow main application entry point."""
import logging
import sys
import time

from src.config import config
from src.providers.weather_underground import WeatherUndergroundProvider
from src.providers.windy import WindyPublisher
from src.providers.idokep import IdokepPublisher


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def validate_config() -> bool:
    """Validate configuration and log any errors."""
    errors = config.validate()
    if errors:
        logger = logging.getLogger(__name__)
        for error in errors:
            logger.error("Configuration error: %s", error)
        return False
    return True


def main() -> None:
    """Main application loop."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("WeatherFlow starting...")
    logger.info("Update interval: %d seconds", config.UPDATE_INTERVAL)
    logger.info("Idokep.hu integration: %s", "enabled" if config.IDOKEP_ENABLED else "disabled")
    
    if not validate_config():
        logger.error("Configuration validation failed. Exiting.")
        sys.exit(1)
    
    # Initialize providers
    wu_provider = WeatherUndergroundProvider()
    windy_publisher = WindyPublisher()
    idokep_publisher = IdokepPublisher()
    
    logger.info("WeatherFlow started successfully")
    
    while True:
        try:
            # Fetch weather data from Weather Underground
            weather_data = wu_provider.fetch()
            
            if weather_data:
                logger.info(
                    "Fetched data: temp=%.1f°C, humidity=%.0f%%, wind=%.1f m/s",
                    weather_data.temp,
                    weather_data.humidity,
                    weather_data.wind_speed,
                )
            
            # Publish to all configured services
            windy_publisher.publish(weather_data)
            idokep_publisher.publish(weather_data)
            
        except Exception as e:
            logger.exception("Unexpected error in main loop: %s", e)
        
        # Wait for the configured interval
        time.sleep(config.UPDATE_INTERVAL)


if __name__ == "__main__":
    main()