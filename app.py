from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():

    city = request.json.get("city")

    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    ).json()

    if "results" not in geo:
        return jsonify({"error":"City not found"})

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    name = geo["results"][0]["name"]

    w = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    ).json()

    current = w["current_weather"]

    return jsonify({
        "city": name,
        "temp": current["temperature"],
        "wind": current["windspeed"],
        "code": current["weathercode"]
    })

if __name__ == "__main__":
    app.run(debug=True)
