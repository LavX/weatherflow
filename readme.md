# 🌦️ WeatherFlow: Multi-Platform Weather Data Forwarding

[![GitHub issues](https://img.shields.io/github/issues/LavX/weatherflow)](https://github.com/LavX/weatherflow/issues)
[![GitHub stars](https://img.shields.io/github/stars/LavX/weatherflow)](https://github.com/LavX/weatherflow/stargazers)
[![GitHub license](https://img.shields.io/github/license/LavX/weatherflow)](https://github.com/LavX/weatherflow/blob/main/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/LavX/weatherflow)](https://github.com/LavX/weatherflow/network)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 Overview

**WeatherFlow** is a modern, Dockerized Python solution that effortlessly transfers your Personal Weather Station (PWS) data from Weather Underground to multiple platforms including Windy and idokep.hu. Leverage the power of APIs and cloud computing to ensure your weather station's data is accurately reflected on multiple platforms, where it can contribute to global and regional weather monitoring.

This project is built with scalability and flexibility in mind, allowing you to configure update intervals and station-specific details with ease. Whether you're a tech enthusiast, a data geek, or a professional meteorologist, WeatherFlow is your go-to solution for seamless weather data integration.

---

## 🚀 Features

- **Dockerized for Simplicity**: Run in a containerized environment for consistent performance across platforms
- **Multi-Platform Support**: Send data to both Windy and idokep.hu simultaneously
- **Modular Architecture**: Clean, maintainable codebase with separate modules for each provider
- **Configurable Update Intervals**: Set your own data update frequency (Windy minimum: 5 minutes)
- **Robust Error Handling**: Comprehensive logging and error handling for reliability
- **Scalable**: Easily deploy multiple instances for managing multiple PWS stations

---

## 📁 Project Structure

```
weatherflow/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── main.py                # Application entry point
│   └── providers/
│       ├── __init__.py
│       ├── weather_underground.py  # WU data fetcher
│       ├── windy.py               # Windy publisher
│       └── idokep.py              # Idokep.hu publisher
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── readme.md
```

---

## 🛠️ Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/LavX/weatherflow.git
    cd weatherflow
    ```

2. **Configure Environment Variables**:
    Update the `docker-compose.yml` with your own values:
    ```yaml
    environment:
      # Required - Weather Underground
      - WU_PWS_ID=your_pws_id_here
      - WU_API_KEY=your_weather_underground_api_key_here
      
      # Required - Windy
      - WINDY_API_KEY=your_windy_api_key_here
      - WINDY_STATION_ID=0
      
      # General settings
      - UPDATE_INTERVAL=300
      
      # Optional - Idokep.hu
      - IDOKEP_ENABLED=false
      - IDOKEP_USER=your_idokep_username
      - IDOKEP_PASS=your_idokep_password
      - IDOKEP_STATION_TYPE=PWS
      - IDOKEP_PRO=false
      - IDOKEP_UTC=1
    ```

3. **Build and Run**:
    ```bash
    docker-compose up -d --build
    ```

4. **Check Logs**:
    ```bash
    docker-compose logs -f
    ```

---

## ⚙️ Configuration Reference

### Required Variables

| Variable | Description |
|----------|-------------|
| `WU_PWS_ID` | Your Weather Underground PWS station ID |
| `WU_API_KEY` | Your Weather Underground API key |
| `WINDY_API_KEY` | Your Windy API key |
| `WINDY_STATION_ID` | Your Windy station ID (default: `0`) |

### General Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `UPDATE_INTERVAL` | Update interval in seconds | `300` (5 minutes) |

### Idokep.hu Settings (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `IDOKEP_ENABLED` | Enable idokep.hu integration | `false` |
| `IDOKEP_USER` | Your idokep.hu username | - |
| `IDOKEP_PASS` | Your idokep.hu password | - |
| `IDOKEP_STATION_TYPE` | Station type (e.g., `PWS`, `WS2305`, `Netatmo`) | `PWS` |
| `IDOKEP_PRO` | Use pro.idokep.hu for data archiving | `false` |
| `IDOKEP_UTC` | Time format: `1` = UTC, `0` = Central European | `1` |

---

## 🇭🇺 Idokep.hu Integration

WeatherFlow supports sending weather data to [idokep.hu](https://www.idokep.hu/), a popular Hungarian weather service.

### Prerequisites

1. Register at [idokep.hu](https://www.idokep.hu/regisztracio) (basic registration is sufficient)
2. For data archiving, register at [pro.idokep.hu](https://pro.idokep.hu/)

### Data Mapping

| Parameter | Description | Unit |
|-----------|-------------|------|
| `hom` | Temperature | °C |
| `rh` | Relative humidity | % |
| `szelirany` | Wind direction | degrees |
| `szelero` | Wind speed | m/s |
| `szellokes` | Wind gust | m/s |
| `p` | Sea-level pressure | hPa |
| `uv` | UV index | - |
| `csap1h` | 1-hour precipitation | mm |

### Notes

- **Temperature 0°C**: Automatically reported as 0.1°C (idokep.hu API limitation)
- **Time Format**: Default is UTC (`IDOKEP_UTC=1`). Set to `0` for Central European local time
- **Pro vs Regular**: Use `IDOKEP_PRO=true` for pro.idokep.hu with data archiving

---

## 🌍 Example Usage

### VEVOR 7-in-1 Wi-Fi Weather Station
- **Weather Underground**: [PWS Dashboard](https://www.wunderground.com/dashboard/pws/ITAKSO6)
- **Windy**: [PWS on Windy](https://www.windy.com/station/pws-f0b1fce0?46.475,19.068,8)

### Docker Commands

```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop service
docker-compose down

# Restart service
docker-compose restart
```

---

## 🔧 Development

### Running Locally (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export WU_PWS_ID=your_pws_id
export WU_API_KEY=your_api_key
export WINDY_API_KEY=your_windy_key
# ... other variables

# Run
python -m src.main
```

### Requirements

- Python 3.14+
- requests >= 2.32.5

---

## 📄 License

Licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 📫 Contact

Questions? [Open an issue](https://github.com/LavX/weatherflow/issues) or reach out via GitHub.

---

**WeatherFlow** - Delivering precise and reliable weather data across platforms ☁️🌧️🌤️

*Crafted with ❤️ by LavX*