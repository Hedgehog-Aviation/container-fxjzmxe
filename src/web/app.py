from flask import Flask, render_template
import requests

app = Flask(__name__)

# HARD-CODED OpenWeather API key
API_KEY = "5cbdeae736ae6506deef3455b4c1f1f2"

# Hope Valley, UK coordinates
LAT = 53.3483
LON = -1.7428

@app.route("/")
def index():
    url = (
        f"https://api.openweathermap.org/data/2.5/onecall"
        f"?lat={LAT}&lon={LON}"
        f"&exclude=current,minutely,hourly,alerts"
        f"&units=metric"
        f"&appid={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    forecast = []
    for day in data.get("daily", []):
        forecast.append({
            "temp_min": day["temp"]["min"],
            "temp_max": day["temp"]["max"],
            "wind_speed": day.get("wind_speed", 0),
            "rain": day.get("rain", 0)
        })

    return render_template("index.html", forecast=forecast)

if __name__ == "__main__":
    app.run(debug=True)
