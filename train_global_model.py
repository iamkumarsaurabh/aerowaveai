import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

print("⏳ Loading Global Weather Dataset...")
df = pd.read_csv("GlobalWeatherRepository.csv")
print(f"📊 Total Records Loaded: {len(df)} rows!")

# SORTING BASED ON LOCATION
df["last_updated"] = pd.to_datetime(df["last_updated"])
df = df.sort_values(by=["location_name", "last_updated"])

# SHIFTING FOR TOMORROW'S DATA
print("⚙️ Processing Multi-Variable Time-Series Data...")
df["tomorrow_temp"] = df.groupby("location_name")["temperature_celsius"].shift(-1)
df["tomorrow_humidity"] = df.groupby("location_name")["humidity"].shift(-1)
df["tomorrow_wind"] = df.groupby("location_name")["wind_kph"].shift(-1)
df["tomorrow_pressure"] = df.groupby("location_name")["pressure_mb"].shift(-1)

df = df.dropna(
    subset=["tomorrow_temp", "tomorrow_humidity", "tomorrow_wind", "tomorrow_pressure"]
)

# PREPARING X (Inputs) AND y (Outputs)
X = df[["temperature_celsius", "humidity", "wind_kph", "pressure_mb"]].rename(
    columns={"temperature_celsius": "temperature"}
)
y = df[["tomorrow_temp", "tomorrow_humidity", "tomorrow_wind", "tomorrow_pressure"]]

# TRAINING THE MODEL
print("🧠 Training the Multi-Output Super Model...")
model = RandomForestRegressor(n_estimators=50, random_state=42)
model.fit(X, y)
print("✅ Global Multi-Variable Model Trained Successfully!")

# SAVING TO PICKLE
model_path = "weather_model.pkl"
with open(model_path, "wb") as file:
    pickle.dump(model, file)

print(f"📁 Model saved successfully as '{model_path}'!")
