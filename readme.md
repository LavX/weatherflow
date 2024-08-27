# 🌦️ Weather Flow: Seamlessly Report Your Peather Underground PWS Data to Windy 🌍

[![GitHub issues](https://img.shields.io/github/issues/LavX/weatherflow)](https://github.com/LavX/weatherflow/issues)
[![GitHub stars](https://img.shields.io/github/stars/LavX/weatherflow)](https://github.com/LavX/weatherflow/stargazers)
[![GitHub license](https://img.shields.io/github/license/LavX/weatherflow)](https://github.com/LavX/weatherflow/blob/main/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/LavX/weatherflow)](https://github.com/LavX/weatherflow/network)

---

## 🌟 Overview

**Weather Flow** is a modern, Dockerized Python solution that effortlessly transfers your Personal Weather Station (PWS) data from Weather Underground to Windy. Leverage the power of APIs and cloud computing to ensure your weather station's data is accurately reflected on Windy, where it can contribute to global weather monitoring.

This project is built with scalability and flexibility in mind, allowing you to configure update intervals and station-specific details with ease. Whether you're a tech enthusiast, a data geek, or a professional meteorologist, Weather Flow is your go-to solution for seamless weather data integration.

---

## 🚀 Features

- **Dockerized for Simplicity**: Run your script in a containerized environment for consistent performance across platforms.
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

Weather Flow is designed to run in the background, continuously syncing data from your PWS to Windy. Customize the update frequency, and add additional PWS stations as needed by tweaking the environment variables.

### Example: Using VEVOR 7-in-1 Wi-Fi Weather Station
- **Weather Underground**: [PWS Dashboard](https://www.wunderground.com/dashboard/pws/ITAKSO6)
- **Windy**: [PWS on Windy](https://www.windy.com/station/pws-f0b1fce0?46.475,19.068,8)

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

