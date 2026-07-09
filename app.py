# api_key = "db44f9d150a209f3d8be517633f4c8e2"

from flask import Flask, render_template, request
import requests
import time
import os
import glob
from datetime import datetime
from audio_engine import generate_weather_audio
from forecast_engine import get_tomorrow_forecast

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def live():
    weather_data = None
    audio_file = None

    if request.method == "POST":
        city = request.form.get("city")

        api_key = "db44f9d150a209f3d8be517633f4c8e2"
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

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
                aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
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
                    "temp": temp,
                    "feels_like": feels_like,
                    "temp_min": temp_min,
                    "temp_max": temp_max,
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

                print("\n" + "=" * 50)
                print(
                    f"🔥 FETCHED DATA FOR: {weather_data['city']}, {weather_data['country']}"
                )
                print("=" * 50)
                for key, value in weather_data.items():
                    print(f"{key.upper():<15}: {value}")
                print("=" * 50 + "\n")

                # CACHE CLEANUP
                search_pattern = os.path.join("static", "weather_*.wav")
                for old_file in glob.glob(search_pattern):
                    if os.path.basename(old_file) != unique_name:
                        try:
                            os.remove(old_file)
                        except Exception as e:
                            print(f"Delete Error: {e}")
            else:
                weather_data = {"error": "City not found! Please check the spelling."}
                print(f"\n❌ ERROR: {weather_data['error']}\n")

        except Exception as e:
            weather_data = {"error": f"API Error: {e}"}
            print(f"\n❌ EXCEPTION CAUGHT: {e}\n")

    return render_template(
        "live.html", weather_data=weather_data, audio_file=audio_file
    )


@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    forecast_data = None

    if request.method == "POST":
        city = request.form.get("city")
        api_key = "db44f9d150a209f3d8be517633f4c8e2"

        # FORECAST ENGINE CALL
        forecast_data = get_tomorrow_forecast(city, api_key)

        print("\n" + "=" * 50)
        print("🧠 AI ML PREDICTION FOR TOMORROW")
        print("=" * 50)
        print(forecast_data)
        print("=" * 50 + "\n")

    return render_template("forecast.html", forecast_data=forecast_data)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
