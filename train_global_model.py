import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle


def train_model():
    df = pd.read_csv("GlobalWeatherRepository.csv")

    # SORTING BASED ON LOCATION
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df = df.sort_values(by=["location_name", "last_updated"])

    # SHIFTING FOR TOMORROW'S DATA
    df["tomorrow_temp"] = df.groupby("location_name")["temperature_celsius"].shift(-1)
    df["tomorrow_humidity"] = df.groupby("location_name")["humidity"].shift(-1)
    df["tomorrow_wind"] = df.groupby("location_name")["wind_kph"].shift(-1)
    df["tomorrow_pressure"] = df.groupby("location_name")["pressure_mb"].shift(-1)

    df = df.dropna(
        subset=[
            "tomorrow_temp",
            "tomorrow_humidity",
            "tomorrow_wind",
            "tomorrow_pressure",
        ]
    )

    # PREPARING X (Inputs) AND y (Outputs)
    X = df[["temperature_celsius", "humidity", "wind_kph", "pressure_mb"]].rename(
        columns={"temperature_celsius": "temperature"}
    )
    y = df[["tomorrow_temp", "tomorrow_humidity", "tomorrow_wind", "tomorrow_pressure"]]

    # TRAINING THE MODEL
    model = RandomForestRegressor(
        n_estimators=40,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X, y)

    # SAVING TO PICKLE
    with open("weather_model.pkl", "wb") as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    train_model()
