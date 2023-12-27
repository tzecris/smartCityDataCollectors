import sys
import requests
import pymongo

# GET current weather and save it for future use

def main(args):
    pre_start()
    return {"msg":"success"}

mongoClient = pymongo.MongoClient('mongodb://172.19.0.6:27017/')
# mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = mongoClient["smartCityDB"]

lat = '37.983922'
lon = '23.725088'
units = 'metric'

APIkey = 'ffa7b61dcf816984a814a15a330e52dd'

urlWeather = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units={units}"

urlPollution = []

def pre_start():
    try:
        start_process(urlWeather)
    except Exception as e:
           print(e)
           print("something went wrong")

def start_process(url):
    url = url.replace("{lat}", lat).replace("{lon}", lon).replace("{API_key}", APIkey).replace("{units}", units)
    print(url)
    response = requests.get(url)
    responseJson = response.json()
    print(responseJson)
    mycol = mydb["liveWeather"]
    result = mycol.insert_one(responseJson)
    print(result)

if __name__ == '__main__':
    main(sys.argv)