import numpy as np
from scipy.io import wavfile
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "sounds")
STATIC_DIR = os.path.join(BASE_DIR, "static")


def force_mono(audio_data):
    if len(audio_data.shape) > 1:
        return np.mean(audio_data, axis=1)
    return audio_data


def generate_weather_audio(condition_desc, temp, wind_speed_kmh, output_filename):
    condition_desc = condition_desc.lower()

    SOUND_MAP = {
        "clear": "spring_forest.wav",
        "sunny": "spring_forest.wav",
        "clouds": "insects_crickets.wav",
        "overcast": "insects_crickets.wav",
        "drizzle": "light_rain.wav",
        "rain": "heavy_rain.wav",
        "thunderstorm": "thunderstorm.wav",
        "snow": "cold_wind.wav",
        "haze": "wind_blowing.wav",
        "mist": "wind_blowing.wav",
        "smoke": "wind_blowing.wav",
        "fog": "cold_wind.wav",
    }

    # DEFAULT AUDIO
    wind_path = os.path.join(ASSETS_DIR, "wind_blowing.wav")
    try:
        sample_rate, final_audio = wavfile.read(wind_path)
        final_audio = force_mono(final_audio)

        wind_volume = min(0.1 + (wind_speed_kmh / 100), 0.3)
        final_audio = final_audio * wind_volume
    except FileNotFoundError:
        return None, "Error"

    matched_file = None
    for key, filename in SOUND_MAP.items():
        if key in condition_desc:
            matched_file = filename
            break

    if matched_file:
        # CONDITION BASED AUDIO
        condition_path = os.path.join(ASSETS_DIR, matched_file)
        try:
            _, condition_audio = wavfile.read(condition_path)
            condition_audio = force_mono(condition_audio)

            # COMBINING BOTH AUDIOS
            min_length = min(len(final_audio), len(condition_audio))
            final_audio = final_audio[:min_length] + (
                condition_audio[:min_length] * 1.5
            )
        except FileNotFoundError:
            matched_file = f"Missing: {matched_file}"
    else:
        matched_file = "Default Wind Only"

    final_audio = np.clip(final_audio, -32768, 32767).astype(np.int16)

    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    output_path = os.path.join(STATIC_DIR, output_filename)
    wavfile.write(output_path, sample_rate, final_audio)

    return output_filename, matched_file
