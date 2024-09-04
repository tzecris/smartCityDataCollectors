import sys
import pymongo
import datetime

mongoClient = pymongo.MongoClient('mongodb://mongo:27017/')
# mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = mongoClient["smartCityDB"]


def main(args):
    if 'collection' in args:
        collection = args['collection']
    else:
        collection = "liveWeatherAvg"

    if 'dateFrom' in args:
        dateFrom = args['dateFrom']
    else:
        dateFrom = '25/12/2022 10:10'

    if 'dateTo' in args:
        dateTo = args['dateTo']
    else:
        dateTo = datetime.datetime.today()

    return start_process(collection, dateFrom, dateTo)


def start_process(collection, dateFrom, dateTo):
    mycol = mydb[collection]
    try:
        if isinstance(dateFrom, str):
            dateFrom = datetime.datetime.strptime(dateFrom, '%d/%m/%Y %H:%M')
        if isinstance(dateTo, str):
            dateTo = datetime.datetime.strptime(dateTo, '%d/%m/%Y %H:%M')
        if collection == 'liveWeather':
            results = mycol.find({'dt': {'$lt': dateTo.timestamp(), '$gte': dateFrom.timestamp()}}, {'_id': False})
        elif collection == 'pollution':
            results = mycol.find({}, {'_id': False})
        else:
            results = mycol.find({'tm': {'$lt': dateTo.timestamp(), '$gte': dateFrom.timestamp()}}, {'_id': False})
        jsonRes = list(results)
        print(jsonRes)
        return {"data": jsonRes}
    except:
        return {"msg": "error something went wrong"}

if __name__ == '__main__':
    main(sys.argv)
