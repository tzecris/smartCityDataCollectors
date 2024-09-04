import sys
import requests

# GET current weather from address

def main(args):
    if 'address' in args:
        address = args['address']
    else:
        address = defaultAddress
    return pre_start(address)


units = 'metric'

APIkey = 'ffa7b61dcf816984a814a15a330e52dd'
APIkeyGeo = '658de81328756347887833xhac6a995'
defaultAddress = "Athens"

urlWeather = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units={units}"
urlGeo = "https://geocode.maps.co/search?q={address}&api_key={API_key}"


def pre_start(address):
    try:
        return getLatLon(address)
    except Exception as e:
        print(e)
        print("something went wrong")
        return {'message': "something went wrong"}


def getWeatherInfo(lat, lon):
    url = urlWeather.replace("{lat}", lat).replace("{lon}", lon).replace("{API_key}", APIkey).replace("{units}", units)
    print(url)
    response = requests.get(url)
    responseJson = response.json()
    print(responseJson)
    return responseJson


def getLatLon(address):
    url = urlGeo.replace("{address}", address).replace("{API_key}", APIkeyGeo)
    print(url)
    response = requests.get(url)
    responseJson = response.json()
    return getWeatherInfo(responseJson[0]["lat"], responseJson[0]["lon"])


if __name__ == '__main__':
    main(sys.argv)
