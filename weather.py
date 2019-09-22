import requests
import json


def wind_description(speed):
    if speed < 1:
        return"calm"
    elif speed < 5:
        return "gentle"
    elif speed < 15:
        return "breezy"
    else:
        return "brisk"

def description(weather_info):
    try:
        id = int(max(list(map(lambda x: x["id"], weather_info))))
        return list(filter(lambda x: (x["id"] == id), weather_info))[0]['description']
    except:
        return ""


url = "http://api.openweathermap.org/data/2.5/weather?zip=19335,us&APPID=248fda902400626e9e74cb2da68f8ad3&units=imperial"
request = requests.get(url)
response = json.loads(request.text)

weather = response["weather"]

condition = response["weather"][0]["description"]
temp = int(response["main"]["temp"])
wind = response["wind"]["speed"]

current_result = f'Good morning, Amy. Outside right now, it is {temp} degrees and {condition}. The winds are {wind_description(wind)}.'
print(current_result)

url = "http://api.openweathermap.org/data/2.5/forecast?zip=19335,us&APPID=248fda902400626e9e74cb2da68f8ad3&units=imperial"
request = requests.get(url)
response = json.loads(request.text)

next_day = response["list"][0:4]
# print(json.dumps(next_day, indent=4))

temps = list(map(lambda x: x["main"]["temp"], next_day))
high_temp = int(max(temps))

winds = list(map(lambda x: x["wind"]["speed"], next_day))
high_wind = int(max(winds))

events = []
for day in next_day:
    for event in day['weather']:
        try:
            events.index(event)
        except:
            events.append(event)
# print(json.dumps(events, indent=4))

weather_desc = []

thunderstorm_info = list(filter(lambda x: (x["id"] > 199) & (x["id"] < 300), events))
weather_desc.append(description(thunderstorm_info))

drizzle_info = list(filter(lambda x: (x["id"] > 299) & (x["id"] < 400), events))
weather_desc.append(description(drizzle_info))

rain_info = list(filter(lambda x: (x["id"] > 499) & (x["id"] < 600), events))
weather_desc.append(description(rain_info))

snow_info = list(filter(lambda x: (x["id"] > 599) & (x["id"] < 700), events))
weather_desc.append(description(snow_info))

atmosphere_info = list(filter(lambda x: (x["id"] > 699) & (x["id"] < 800), events))
weather_desc.append(description(atmosphere_info))

cloud_info = list(filter(lambda x: (x["id"] > 799) & (x["id"] < 900), events))
weather_desc.append(description(cloud_info))

weather_desc = list(filter(lambda x: x!="", weather_desc))
weather_summary = ", ".join(weather_desc)

overnight = response["list"][2:6]
temps = list(map(lambda x: x["main"]["temp"], overnight))
low_temp = int(min(temps))

forecast_result = f'The high today will be {high_temp} degrees. Also, expect {weather_summary} and winds will be {wind_description(high_wind)}. The low overnight will be {low_temp}'
print(forecast_result)
