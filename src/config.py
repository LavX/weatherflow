"""Configuration management for WeatherFlow."""
import os


class Config:
    """Application configuration loaded from environment variables."""
    
    # Weather Underground settings
    WU_PWS_ID: str = os.getenv('WU_PWS_ID', '')
    WU_API_KEY: str = os.getenv('WU_API_KEY', '')
    
    # Windy settings
    WINDY_API_KEY: str = os.getenv('WINDY_API_KEY', '')
    WINDY_STATION_ID: int = int(os.getenv('WINDY_STATION_ID', '0'))
    
    # Idokep.hu settings
    IDOKEP_ENABLED: bool = os.getenv('IDOKEP_ENABLED', 'false').lower() == 'true'
    IDOKEP_USER: str = os.getenv('IDOKEP_USER', '')
    IDOKEP_PASS: str = os.getenv('IDOKEP_PASS', '')
    IDOKEP_STATION_TYPE: str = os.getenv('IDOKEP_STATION_TYPE', 'PWS')
    IDOKEP_PRO: bool = os.getenv('IDOKEP_PRO', 'false').lower() == 'true'
    IDOKEP_UTC: int = int(os.getenv('IDOKEP_UTC', '1'))
    
    # Update interval in seconds
    UPDATE_INTERVAL: int = int(os.getenv('UPDATE_INTERVAL', '300'))
    
    @classmethod
    def get_wu_url(cls) -> str:
        """Get Weather Underground API URL."""
        return (
            f"https://api.weather.com/v2/pws/observations/current"
            f"?stationId={cls.WU_PWS_ID}"
            f"&format=json&units=m&numericPrecision=decimal"
            f"&apiKey={cls.WU_API_KEY}"
        )
    
    @classmethod
    def get_windy_url(cls) -> str:
        """Get Windy API URL."""
        return f"https://stations.windy.com/pws/update/{cls.WINDY_API_KEY}"
    
    @classmethod
    def get_idokep_url(cls) -> str:
        """Get Idokep.hu API URL based on pro setting."""
        if cls.IDOKEP_PRO:
            return "https://pro.idokep.hu/sendws.php"
        return "https://automata.idokep.hu/sendws.php"
    
    @classmethod
    def validate(cls) -> list:
        """Validate required configuration and return list of errors."""
        errors: list[str] = []
        
        if not cls.WU_PWS_ID:
            errors.append("WU_PWS_ID is required")
        if not cls.WU_API_KEY:
            errors.append("WU_API_KEY is required")
        if not cls.WINDY_API_KEY:
            errors.append("WINDY_API_KEY is required")
        
        if cls.IDOKEP_ENABLED:
            if not cls.IDOKEP_USER:
                errors.append("IDOKEP_USER is required when IDOKEP_ENABLED=true")
            if not cls.IDOKEP_PASS:
                errors.append("IDOKEP_PASS is required when IDOKEP_ENABLED=true")
        
        return errors


config = Config()