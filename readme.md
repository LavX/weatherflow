# 🌦️ Weather Flow: Seamlessly Report Your Weather Underground PWS Data to Windy 🌍

[![GitHub issues](https://img.shields.io/github/issues/LavX/weatherflow)](https://github.com/LavX/weatherflow/issues)
[![GitHub stars](https://img.shields.io/github/stars/LavX/weatherflow)](https://github.com/LavX/weatherflow/stargazers)
[![GitHub license](https://img.shields.io/github/license/LavX/weatherflow)](https://github.com/LavX/weatherflow/blob/main/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/LavX/weatherflow)](https://github.com/LavX/weatherflow/network)

---

## 🌟 Overview

**Weather Flow** is a modern, Dockerized Python solution that effortlessly transfers your Personal Weather Station (PWS) data from Weather Underground to Windy and idokep.hu. Leverage the power of APIs and cloud computing to ensure your weather station's data is accurately reflected on multiple platforms, where it can contribute to global and regional weather monitoring.

This project is built with scalability and flexibility in mind, allowing you to configure update intervals and station-specific details with ease. Whether you're a tech enthusiast, a data geek, or a professional meteorologist, Weather Flow is your go-to solution for seamless weather data integration.

---

## 🚀 Features

- **Dockerized for Simplicity**: Run your script in a containerized environment for consistent performance across platforms.
- **Multi-Platform Support**: Send data to both Windy and idokep.hu simultaneously.
- **Configurable Update Intervals**: Set your own data update frequency via environment variables. (Windy restriction is 5 or more minutes!)
- **Robust Error Handling**: Logs and retries failed requests to maintain data integrity.
- **Scalable**: Easily deploy multiple instances if managing data for more than one PWS.

---

## 🛠️ Setup

### Prerequisites

Ensure you have the following installed:
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
    ```env
    WU_PWS_ID=your_pws_id_here
    WU_API_KEY=your_weather_underground_api_key_here
    WINDY_API_KEY=your_windy_api_key_here
    WINDY_STATION_ID=0
    UPDATE_INTERVAL=300
    # Idokep.hu settings (optional)
    IDOKEP_ENABLED=true
    IDOKEP_USER=your_idokep_username
    IDOKEP_PASS=your_idokep_password
    IDOKEP_STATION_TYPE=PWS
    IDOKEP_PRO=false
    IDOKEP_UTC=1
    ```

3. **Build and Run**:
    ```bash
    docker-compose up -d --build
    ```

4. **Check Logs**:
    Monitor the service to ensure data is being sent correctly:
    ```bash
    docker-compose logs -f
    ```

---

## 🌍 Usage

Weather Flow is designed to run in the background, continuously syncing data from your PWS to Windy and idokep.hu. Customize the update frequency, and add additional PWS stations as needed by tweaking the environment variables.

### Example: Using VEVOR 7-in-1 Wi-Fi Weather Station
- **Weather Underground**: [PWS Dashboard](https://www.wunderground.com/dashboard/pws/ITAKSO6)
- **Windy**: [PWS on Windy](https://www.windy.com/station/pws-f0b1fce0?46.475,19.068,8)

---

## 🇭🇺 Idokep.hu Integration

Weather Flow now supports sending weather data to [idokep.hu](https://www.idokep.hu/), a popular Hungarian weather service. This feature is optional and can be enabled via environment variables.

### Prerequisites for Idokep.hu

1. Register an account at [idokep.hu](https://www.idokep.hu/regisztracio) (basic registration is sufficient for data upload)
2. For data archiving, register at [pro.idokep.hu](https://pro.idokep.hu/) (in this case, the API endpoint changes to `pro.idokep.hu`)

### Idokep.hu Configuration

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `IDOKEP_ENABLED` | Set to `true` to enable idokep.hu integration | Yes | `false` |
| `IDOKEP_USER` | Your idokep.hu username | Yes (if enabled) | - |
| `IDOKEP_PASS` | Your idokep.hu password | Yes (if enabled) | - |
| `IDOKEP_STATION_TYPE` | The type of your weather station (e.g., `PWS`, `WS2305`, `Netatmo`) | No | `PWS` |
| `IDOKEP_PRO` | Set to `true` to use pro.idokep.hu (for data archiving) | No | `false` |
| `IDOKEP_UTC` | Time format: `1` = UTC, `0` = Central European local time | No | `1` |

### Update Frequency

Data is sent to idokep.hu at the same interval as Windy, controlled by the `UPDATE_INTERVAL` environment variable (default: 300 seconds = 5 minutes). Both services receive data simultaneously in each update cycle.

### Data Mapping

The following data is sent to idokep.hu:

| Idokep.hu Parameter | Description | Source |
|---------------------|-------------|--------|
| `hom` | Temperature (°C) | Weather Underground temp |
| `rh` | Relative humidity (%) | Weather Underground humidity |
| `szelirany` | Wind direction (degrees) | Weather Underground winddir |
| `szelero` | Wind speed (m/s) | Weather Underground windSpeed |
| `szellokes` | Wind gust (m/s) | Weather Underground windGust |
| `p` | Sea-level pressure (hPa) | Weather Underground pressure |
| `uv` | UV index | Weather Underground UV |
| `csap1h` | 1-hour precipitation (mm) | Weather Underground precipRate |

### Notes

- **Temperature 0°C**: Idokep.hu API doesn't accept exactly 0.0°C. If the temperature is 0.0°C, it will be automatically reported as 0.1°C.
- **Time Format**: By default, data is sent with UTC timestamps (`IDOKEP_UTC=1`). If your server is already in UTC and you prefer to send local Central European time, set `IDOKEP_UTC=0`.
- **Pro vs Regular**: Use `IDOKEP_PRO=true` if you have a pro.idokep.hu account and want data archiving. Otherwise, leave it as `false` to use the standard automata.idokep.hu endpoint.

### Example Commands

- **Rebuild and Restart**:
    ```bash
    docker-compose up -d --build
    ```
- **Stop the Service**:
    ```bash
    docker-compose down
    ```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/LavX/weatherflow/blob/main/LICENSE) file for details.

---

## 📫 Contact

Have questions? Feel free to [open an issue](https://github.com/LavX/weatherflow/issues) or reach out directly via GitHub.

---

**Weather Flow** is part of the modern tech stack for weather enthusiasts, delivering precise and reliable weather data to Windy. Join the movement, and let's make the weather world a bit more accurate! ☁️🌧️🌤️

---

This README was crafted with ❤️ by LavX.

---

