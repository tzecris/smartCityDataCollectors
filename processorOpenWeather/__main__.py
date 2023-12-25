import sys
import requests
import pymongo
from datetime import date

# GET current weather and save it for future use
# NOT TESTED

def main(args):
    pre_start()
    return {"msg":"success"}

mongoClient = pymongo.MongoClient('mongodb://172.17.0.1:27017/')
mydb = mongoClient["smartCityDB"]

urlPollution = []

def pre_start():
    try:
        start_process()
    except Exception as e:
           print(e)
           print("something went wrong")

def start_process():
    today = date.today()

    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    
    mycol = mydb["liveWeather" + d1]
    result = mycol.insert_one()
    print(result)

if __name__ == '__main__':
    main(sys.argv)
