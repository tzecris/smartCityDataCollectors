import sys
import pandas as pd
import json
import pymongo
from minio import Minio
from io import BytesIO

# client = Minio("127.0.0.1:9000",access_key="GpctiYhJEJjRG8r0",secret_key="DhIMWMz43uRWyhXQ0CkFMRaQtv6LWe1T",secure=False)
# client = Minio("172.17.0.2:9000",access_key="GpctiYhJEJjRG8r0",secret_key="DhIMWMz43uRWyhXQ0CkFMRaQtv6LWe1T",secure=False)
client = Minio("172.17.0.2:9000",access_key="1mrwuetKJr7XrBtN",secret_key="OHkccz5pCQ3eVyFHTfSOtGWDtx2zrv32",secure=False)

mongoClient = pymongo.MongoClient('mongodb://localhost:27017/',
                     username='user',
                     password='pass')
mydb = mongoClient["smartCityDB"]

def connect_minio(args):
    print(args)

    if client.bucket_exists("pollution"):
        try:
            objects = client.list_objects("pollution")

            for item in objects:

                raw_data = client.list_objects("pollution")

                for df in raw_data:
                    raw_file = client.get_object(df.bucket_name, df.object_name)
                    df_csv = pd.read_csv(raw_file)
                    start_process(df_csv, df.object_name)
        except Exception as e:
           print(e)
           print("error on reading file")

    else:
        print("this bucket does not exist")


def start_process(df_csv, file_name):
    start_date = df_csv.head(1)['timestamp']
    end_date = df_csv.tail(1)['timestamp']
    # print(start_date)
    # print(end_date)


    index_labels=['ozone','particullate_matter','carbon_monoxide','sulfure_dioxide','nitrogen_dioxide']
    df_csv = df_csv.filter(items=index_labels)
    df = pd.DataFrame(df_csv)
    # print(df)

    dfAll = df.mean()
    max = df.max(axis=0)
    min = df.min(axis=0)
    # print("max:")
    # print(max)
    # print("min:")
    # print(min)

    # print("ne w ALL: ")
    # print(dfAll)
    results_csv = dfAll.T.to_csv().encode('utf-8')

    records = dfAll.to_dict()
    recordsMin = min.to_dict()
    recordsMax = max.to_dict()

    dfAll["start_date"] = start_date.values[0]
    dfAll["end_date"] = end_date.values[0]
    print(records)
    print(recordsMax)
    print(recordsMin)
    # mycol = mydb["pollution"]
    # result = mycol.insert_one(records)
    # print(result)

    # # output to csv files
    # client.put_object(
	# "results",
	# "/" + file_name + ".csv",
	# data=BytesIO(results_csv),
	# length=len(results_csv),
	# content_type='application/csv'
    # )


def main(args):
    connect_minio(args)
    return {"msg":"success"}


if __name__ == '__main__':
    main(sys.argv)
