import pandas as pd

# CSV file ko read kar rahe hain
df = pd.read_csv("GlobalWeatherRepository.csv")

# Sirf columns ke naam print karwa rahe hain
print("📊 CSV Columns:", df.columns.tolist())
