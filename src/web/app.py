from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

LAT = 53.3483
LON = -1.7428

@app.route("/")
def index():
    error = None
    forecast = []

    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={LAT}"
            f"&longitude={LON}"
            "&daily=temperature_2m_min,temperature_2m_max,"
            "precipitation_sum,windspeed_10m_max"
            "&timezone=Europe/London"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP errors

        data = response.json()

        if "daily" not in data:
            raise ValueError(f"Unexpected API response: {data}")

        daily = data["daily"]

        for i in range(len(daily["time"])):
            forecast.append({
                "date": datetime.fromisoformat(daily["time"][i]).strftime("%A, %d %b"),
                "temp_min": daily["temperature_2m_min"][i],
                "temp_max": daily["temperature_2m_max"][i],
                "wind_speed": daily["windspeed_10m_max"][i],
                "rain": daily["precipitation_sum"][i]
            })

    except Exception as e:
        error = str(e)

    return render_template(
        "index.html",
        forecast=forecast,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
