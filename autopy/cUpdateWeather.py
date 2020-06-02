import requests
import json
import urllib3
from datetime import datetime
import pdb

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

weather_dict = {}

def get_weather_forecast():
    print("Updating Weather")

    wIcons = {
        "clear-day": "https://developer.accuweather.com/sites/default/files/01-s.png",
        "clear-night": "https://developer.accuweather.com/sites/default/files/33-s.png",
        "rain": "https://developer.accuweather.com/sites/default/files/18-s.png",
        "wind": "https://developer.accuweather.com/sites/default/files/32-s.png",
        "fog": "https://developer.accuweather.com/sites/default/files/11-s.png",
        "cloudy": "https://developer.accuweather.com/sites/default/files/07-s.png",
        "partly-cloudy-day": "https://developer.accuweather.com/sites/default/files/06-s.png",
        "partly-cloudy-night": "https://developer.accuweather.com/sites/default/files/35-s.png"
    }

    try:
        darkSkyURL = "url with key here"

        currentWeather = requests.get(darkSkyURL)
	#pdb.set_trace()
        currentData = currentWeather.json()

        weather_location = 'Peoria'
        weather_state = 'AZ'
        weather_currentTemp = currentData["currently"]["temperature"]
        weather_currentHumidity = currentData["currently"]["humidity"] * 100
        weather_currentWind= currentData["currently"]["windSpeed"]
        weather_currentGust = currentData["currently"]["windGust"]
        weather_currentFeelsLike = currentData["currently"]["apparentTemperature"]
        weather_currentSolarRadiation = "-"
        weather_currentUv = currentData["currently"]["uvIndex"]
        weather_currentIcon = wIcons[currentData["currently"]["icon"]]

        weather_dict['weatherDataCurrent'] = "{},{},{},{},{},{},{},{},{},{}".format(weather_location, weather_state, weather_currentIcon, weather_currentSolarRadiation, weather_currentHumidity, weather_currentFeelsLike, weather_currentUv, weather_currentWind, weather_currentTemp, weather_currentGust)

        obj_count = 0

        for obj in currentData['daily']['data']:
            if obj_count < 4:
                timeStamp = int(obj['time'])
                dateTimeStamp = datetime.utcfromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
                dto = datetime.strptime( dateTimeStamp.split(" ")[0], '%Y-%m-%d')
                dow = dto.strftime("%A")

                dict_key = "weatherDataDay{}".format(obj_count)

                weather_dict[dict_key] = "{},{},{},{},{},{},{},{},{},{},{},{}".format(obj["temperatureHigh"],
                                                                dow,
                                                                obj["windSpeed"],
                                                                dow,
                                                                obj["windGust"],
                                                                obj["humidity"] * 100,
                                                                "{} - wind {} mph  high {}F".format(obj["summary"] ,obj["windSpeed"], obj["temperatureHigh"]),
                                                                wIcons[obj["icon"]],
                                                                "-",
                                                                obj["temperatureLow"],
                                                                "-",
                                                                "low {}F".format(obj["temperatureLow"]))

                obj_count += 1

    except IOError:
        print("Connection Error")
        pass


def send_info():
    url = "https://www.goff.us/api/weather/"

    header_data = {
        "Content-Type":"application/json",
	    'Accept-Encoding': "gzip, deflate",
        'Authorization': 'Bearer Bearer token here'
    }

    weather_json = json.dumps(weather_dict)
    response = requests.post(url, headers=header_data, verify=False, data=weather_json)
    # print(weather_json)

get_weather_forecast()
send_info()
