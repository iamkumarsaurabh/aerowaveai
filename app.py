import os
from flask import Flask, render_template, request
import requests
import time
import glob
from datetime import datetime
from audio_engine import generate_weather_audio
from forecast_engine import get_tomorrow_forecast

app = Flask(__name__)

API_KEY = os.environ.get("OPENWEATHER_API_KEY")


@app.route("/", methods=["GET", "POST"])
def live():
    weather_data = None
    audio_file = None

    if request.method == "POST":
        city = request.form.get("city")
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            # API CALL for Current Weather Data
            response = requests.get(weather_url)
            data = response.json()

            if response.status_code == 200:
                condition = data["weather"][0]["main"]
                description = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                temp_min = data["main"]["temp_min"]
                temp_max = data["main"]["temp_max"]
                pressure = data["main"]["pressure"]
                humidity = data["main"]["humidity"]
                wind_speed = round(data["wind"]["speed"] * 3.6, 2)
                visibility = data.get("visibility", 0) / 1000
                sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime(
                    "%I:%M %p"
                )
                sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime(
                    "%I:%M %p"
                )

                lat = data["coord"]["lat"]
                lon = data["coord"]["lon"]

                # API CALL for AQI Data
                aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
                aqi_response = requests.get(aqi_url).json()

                aqi_value = aqi_response["list"][0]["main"]["aqi"]

                aqi_mapping = {
                    1: "Good 🟢",
                    2: "Fair 🟡",
                    3: "Moderate 🟠",
                    4: "Poor 🔴",
                    5: "Very Poor 🟤",
                }
                aqi_text = aqi_mapping.get(aqi_value, "Unknown")

                from datetime import timezone, timedelta

                utc_now = datetime.now(timezone.utc)
                city_time = utc_now + timedelta(seconds=data["timezone"])
                local_hour = city_time.hour

                # AUDIO ENGINE CALL
                unique_name = f"weather_{int(time.time())}.wav"
                audio_file, active_layer = generate_weather_audio(
                    condition, temp, wind_speed, unique_name
                )

                weather_data = {
                    "city": data["name"],
                    "country": data["sys"].get("country", ""),
                    "condition": condition,
                    "description": description,
                    "temp": round(temp, 1),
                    "feels_like": round(feels_like, 1),
                    "temp_min": round(temp_min, 1),
                    "temp_max": round(temp_max, 1),
                    "humidity": humidity,
                    "pressure": pressure,
                    "visibility_km": visibility,
                    "wind_speed": wind_speed,
                    "sunrise": sunrise,
                    "sunset": sunset,
                    "aqi_status": aqi_text,
                    "local_hour": local_hour,
                    "active_layer": active_layer.replace(".wav", "")
                    .replace("_", " ")
                    .title(),
                }

                # CACHE CLEANUP
                search_pattern = os.path.join("static", "weather_*.wav")
                for old_file in glob.glob(search_pattern):
                    if os.path.basename(old_file) != unique_name:
                        try:
                            os.remove(old_file)
                        except Exception:
                            pass
            else:
                weather_data = {"error": "City not found! Please check the spelling."}

        except Exception as e:
            weather_data = {"error": f"API Error: {e}"}

    return render_template(
        "live.html", weather_data=weather_data, audio_file=audio_file
    )


@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    forecast_data = None

    if request.method == "POST":
        city = request.form.get("city")

        # FORECAST ENGINE CALL
        forecast_data = get_tomorrow_forecast(city, API_KEY)

    return render_template("forecast.html", forecast_data=forecast_data)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)