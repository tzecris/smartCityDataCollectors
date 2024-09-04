import sys
import pandas as pd
import pymongo
from minio import Minio

client = Minio("minio:9000", "5VCTEQOQ0GR0NV1T67GN", "8MBK5aJTR330V1sohz4n1i7W5Wv/jzahARNHUzi3", secure=False)
# client = Minio("127.0.0.1:9003", "minio99", "minio123", secure=False)

# mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
mongoClient = pymongo.MongoClient('mongodb://mongo:27017/')

mydb = mongoClient["smartCityDB"]


def connect_minio(args):
    print(args)

    if 'bucket' in args:
        bucket = args['bucket']
    else:
        bucket = "pollution"

    if 'filepath' in args:
        filepaths = args['filepath']
    else:
        print("file path required")
        return {"error": "file path required"}
        # filepath = '2023-12-31T21:02:53.648454'

    if client.bucket_exists(bucket):
        try:
            for filepath in filepaths:
                # "my-bucket", prefix="my/prefix/", recursive=True,
                objects = client.list_objects(bucket, prefix=filepath + '/', recursive=True)

                for obj in objects:
                    raw_file = client.get_object(obj.bucket_name, obj.object_name)
                    df_csv = pd.read_csv(raw_file)
                    start_process(df_csv, obj.object_name, bucket)

            return {"msg": "success"}
        except Exception as e:
            print(e)
            print("error on reading file")
            return {"error": "error on reading file"}

    else:
        print("this bucket does not exist")
        return {"error": "this bucket does not exist"}


def list_folder_reader(bn, name):
    return client.list_objects(bn, name)


def start_process(df_csv, file_name, bucket):
    start_date = df_csv.head(1)['timestamp']
    end_date = df_csv.tail(1)['timestamp']

    index_labels = ['ozone', 'particullate_matter', 'carbon_monoxide', 'sulfure_dioxide', 'nitrogen_dioxide']
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
    # results_csv = dfAll.T.to_csv().encode('utf-8')

    records = dfAll.to_dict()
    recordsMin = min.to_dict()
    recordsMax = max.to_dict()

    records["start_date"] = start_date.values[0]
    records["end_date"] = end_date.values[0]

    # print(records)
    # print(recordsMax)
    # print(recordsMin)
    mycol = mydb[bucket]
    records['_id'] = file_name
    result = mycol.insert_one(records)
    # print(result)


def main(args):
    return connect_minio(args)


if __name__ == '__main__':
    main(sys.argv)
