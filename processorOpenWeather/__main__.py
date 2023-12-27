import collections
import sys
import pymongo
import datetime

def main(args):
    pre_start()
    return {'msg': 'success'}


# mongoClient = pymongo.MongoClient('mongodb://172.19.0.6:27017/')
mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = mongoClient["smartCityDB"]
mycol = mydb["liveWeather"]
mycolAvg = mydb["liveWeatherAvg"]


urlPollution = []


def pre_start():
    try:
        start_process()
    except Exception as e:
        print(e)
        print("something went wrong")


def start_process():
    today = datetime.datetime.today()
    # end = datetime.datetime(today.year, today.month, today.day, 00, 00, 00)
    end = today
    start = end - datetime.timedelta(hours=2)

    print('end:')
    print(end.timestamp())
    print('start:')
    print(start.timestamp())

    results = mycol.find({'dt': {'$lt': end.timestamp(), '$gte': start.timestamp()}})

    weatherInfo = collections.defaultdict(list)

    for result in results:
        weatherInfo['temp'].append(float(result['main']['temp']))
        weatherInfo['feels_like'].append(float(result['main']['feels_like']))
        weatherInfo['pressure'].append(int(result['main']['pressure']))
        weatherInfo['humidity'].append(float(result['main']['humidity']))

    averages = {sub: sum(scores)/len(scores) for sub, scores in weatherInfo.items()}
    averages['tm'] = today.timestamp()
    result = mycolAvg.insert_one(averages)
    print(result)


if __name__ == '__main__':
    main(sys.argv)
