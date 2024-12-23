from flask import Flask, render_template, request, redirect
from weather_api import get_city_coordinates, get_weather_data

app = Flask(__name__)
cities = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global cities
    if request.method == 'POST':
        start_point = request.form['start_point']
        end_point = request.form['end_point']
        intermediate_cities = request.form.getlist('intermediate_city')
        cities = [start_point, end_point] + intermediate_cities
        return redirect('/weather/')
    return render_template('index.html')

@app.route('/weather/')
def weather():
    weather_data = {}
    for city in cities:
        data = get_weather_data(city, 3)
        if data is not None:
            weather_data[city] = {
                'temperature': data['temperature'].tolist(),
                'wind_speed': data['wind_speed'].tolist(),
                'precipitation': data['precipitation'].tolist(),
                'coordinates': get_city_coordinates(city)
            }
    return render_template('weather.html', weather_data=weather_data, cities=cities)

if __name__ == "__main__":
    app.run(port=8000)