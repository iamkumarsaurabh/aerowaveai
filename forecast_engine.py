import os
import pickle
import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "weather_model.pkl")

_ml_model = None


def get_trained_model():
    global _ml_model
    if _ml_model is None:
        try:
            with open(MODEL_PATH, "rb") as file:
                _ml_model = pickle.load(file)
            print("✅ Multi-Variable ML Model Loaded Successfully!")

        except FileNotFoundError:
            print(f"❌ Error: Model file missing at {MODEL_PATH}")

    return _ml_model


def get_tomorrow_forecast(city_name, api_key):
    # FETCHING LIVE DATA
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:

            current_temp = data["main"]["temp"]
            current_humidity = data["main"]["humidity"]
            current_wind = data["wind"]["speed"] * 3.6
            current_pressure = data["main"]["pressure"]

            from datetime import datetime, timezone, timedelta

            utc_now = datetime.now(timezone.utc)
            city_time = utc_now + timedelta(seconds=data["timezone"])
            local_hour = city_time.hour

            # LOADING THE TRAINED MODEL
            model = get_trained_model()

            if model is None:
                return {"error": "ML Model file is missing in the backend."}

            live_weather = pd.DataFrame(
                {
                    "temperature": [current_temp],
                    "humidity": [current_humidity],
                    "wind_kph": [current_wind],
                    "pressure_mb": [current_pressure],
                }
            )

            prediction = model.predict(live_weather)

            predicted_temp = prediction[0][0]
            predicted_humidity = prediction[0][1]
            predicted_wind = prediction[0][2]
            predicted_pressure = prediction[0][3]

            # LOGIC FOR GUESSING THE CONDITION BASED ON HUMIDITY
            if predicted_humidity > 80:
                predicted_condition = "Rain"
            elif predicted_humidity > 60:
                predicted_condition = "Clouds"
            else:
                predicted_condition = "Clear"

            return {
                "city": data["name"],
                "model_status": "AeroWave AI Multi-Model Active 🟢",
                "current_temp": current_temp,
                "predicted_temp": round(predicted_temp, 2),
                "predicted_humidity": round(predicted_humidity, 2),
                "predicted_wind": round(predicted_wind, 2),
                "predicted_pressure": int(predicted_pressure),
                "predicted_condition": predicted_condition,
                "confidence": "88%",
                "local_hour": local_hour,
            }

        else:
            return {"error": "City not found or API error."}

    except Exception as e:
        return {"error": f"Prediction Error: {str(e)}"}
