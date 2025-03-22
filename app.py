from flask import Flask, request, jsonify  
import requests  

app = Flask(__name__) 

# Home Route - This will fix the 404 error when visiting http://127.0.0.1:5000/
@app.route('/')  
def home():  
    return "Weather API is Running! Use /weather?city=CityName to get data."

# Replace with your actual API key  
API_KEY = "914dad333009e175950e326b22ac6410"  

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    unit = request.args.get('unit', 'metric')  # Default = metric (Celsius)

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return jsonify({"error": "Invalid city name or API issue"}), 400

    # Unit symbol setup
    temp_unit = "°C" if unit == "metric" else "°F"

    # Improved output format
    weather_data = {
        "City": data["name"],
        "Temperature": f"{data['main']['temp']}{temp_unit}",
        "Weather Condition": data["weather"][0]["description"].title(),
        "Humidity": f"{data['main']['humidity']}%",
        "Wind Speed": f"{data['wind']['speed']} m/s"
    }

    return jsonify(weather_data)
 

if __name__ == '__main__':  
    app.run(debug=True)  
