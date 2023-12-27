import sys
from zipfile import ZipFile
from minio import Minio
from io import BytesIO
import tarfile
from urllib.request import urlopen, urlretrieve
from datetime import datetime

urlWeather = ["http://iot.ee.surrey.ac.uk:8080/datasets/weather/feb_jun_2014/raw_weather_data_aarhus.tar.gz",
              "http://iot.ee.surrey.ac.uk:8080/datasets/weather/aug_sep_2014/raw_weather_data_aug_sep_2014.zip"
              ]

urlPollution = [
    "http://iot.ee.surrey.ac.uk:8080/datasets/pollution/citypulse_pollution_csv_data_aarhus_aug_oct_2014.tar.gz"]

# client = Minio("172.17.0.2:9000","minio99","minio123",secure=False)
# client = Minio("127.0.0.1:9000", access_key="5VCTEQOQ0GR0NV1T67GN", secret_key="8MBK5aJTR330V1sohz4n1i7W5Wv/jzahARNHUzi3",
#                secure=False)


client = Minio("127.0.0.1:9003","minio99","minio123",secure=False)

def connect_minio(dataType):
    if dataType == 'weather':
        dataUrl = urlWeather
        contentType = 'text/plain'
    elif dataType == 'pollution':
        dataUrl = urlPollution
        contentType = 'application/csv'
    else:
        dataUrl = urlWeather
        contentType = 'text/plain'

    if client.bucket_exists(dataType):
        try:
            for url in dataUrl:
                start_process(url, dataType, contentType)
        except Exception as e:
            print(e)
            print("something went wrong")

    else:
        print("this bucket does not exist")


def saveToMinio(name, tfile, current_dateTime, dataType, contentType, isZip):
    print(name)

    if (isZip):
        file = tfile.open(name)
    else:
        file = tfile.extractfile(name)

    content = file.read()
    fileName = current_dateTime.isoformat() + '/' + name

    client.put_object(
        dataType,
        fileName,
        data=BytesIO(content),
        length=len(content),
        content_type=contentType
    )


def start_process(url, dataType, contentType):
    current_dateTime = datetime.now()

    if (url.endswith(".tar.gz")):
        ftpstream = urlopen(url)
        tmpfile = BytesIO()
        while True:
            s = ftpstream.read()
            if not s:
                break
            tmpfile.write(s)
        ftpstream.close()
        tmpfile.seek(0)
        tfile = tarfile.open(fileobj=tmpfile, mode="r:gz")

        for name in tfile.getnames():
            saveToMinio(name, tfile, current_dateTime, dataType, contentType, False)

        tfile.close()
        tmpfile.close()

    elif (url.endswith(".zip")):
        filehandle, _ = urlretrieve(url)
        tfile = ZipFile(filehandle, 'r')

        for name in tfile.namelist():
            saveToMinio(name, tfile, current_dateTime, dataType, contentType, True)

        tfile.close()


def main(args):
    if 'type' in args:
        dataType = args['type']
    else:
        dataType = "weather"
    connect_minio(dataType)
    return {"msg": "success",
            "dataType": dataType,
            "args": args
            }


if __name__ == '__main__':
    main(sys.argv)
