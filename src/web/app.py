from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

LAT = 53.3482
LON = -1.7449

@app.route("/")
def index():
    error = None
    current = None
    hourly = []

    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={LAT}"
            f"&longitude={LON}"
            "&current=temperature_2m,apparent_temperature,"
            "wind_speed_10m,wind_direction_10m,"
            "wind_gusts_10m,precipitation"
            "&hourly=temperature_2m,apparent_temperature,"
            "precipitation_probability,precipitation,"
            "wind_speed_10m,wind_speed_180m,"
            "wind_direction_10m,wind_direction_180m"
            "&timezone=Europe/London"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # ---- CURRENT WEATHER ----
        if "current" not in data:
            raise ValueError(f"Missing current weather data: {data}")

        current = data["current"]

        # ---- HOURLY WEATHER ----
        if "hourly" not in data:
            raise ValueError(f"Missing hourly weather data: {data}")

        hourly_data = data["hourly"]

        times = hourly_data["time"]
        count = len(times)

        for i in range(count):
            hourly.append({
                "time": datetime.fromisoformat(times[i]).strftime("%a %H:%M"),
                "temperature": hourly_data["temperature_2m"][i],
                "apparent_temperature": hourly_data["apparent_temperature"][i],
                "precip_prob": hourly_data["precipitation_probability"][i],
                "precip": hourly_data["precipitation"][i],
                "wind_10m": hourly_data["wind_speed_10m"][i],
                "wind_180m": hourly_data["wind_speed_180m"][i],
                "wind_dir_10m": hourly_data["wind_direction_10m"][i],
                "wind_dir_180m": hourly_data["wind_direction_180m"][i],
            })

    except Exception as e:
        error = str(e)

    return render_template(
        "index.html",
        error=error,
        current=current,
        hourly=hourly
    )

if __name__ == "__main__":
    app.run(debug=True)
