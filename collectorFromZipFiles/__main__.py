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

client = Minio("minio:9000", "5VCTEQOQ0GR0NV1T67GN", "8MBK5aJTR330V1sohz4n1i7W5Wv/jzahARNHUzi3",secure=False)
# client = Minio("127.0.0.1:9003", "minio99", "minio123", secure=False)


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

    print('connect minio')
    if not client.bucket_exists(dataType):
        client.make_bucket(dataType)

    paths = []
    for url in dataUrl:
        print(url)
        current_dateTime = datetime.now()
        start_process(url, dataType, contentType, current_dateTime)
        paths.append(current_dateTime.isoformat())

    return paths


def saveToMinio(name, tfile, current_dateTime, dataType, contentType, isZip):
    print(name)

    if "MACOSX" in name:
        return

    if (isZip):
        file = tfile.open(name)
    else:
        file = tfile.extractfile(name)

    content = file.read()

    if "/" in name:
        name = name.split("/")[1]
    fileName = current_dateTime.isoformat() + '/' + name

    client.put_object(
        dataType,
        fileName,
        data=BytesIO(content),
        length=len(content),
        content_type=contentType
    )


def start_process(url, dataType, contentType, current_dateTime):
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

    try:
        print(dataType)
        filepath = connect_minio(dataType)
        json={"msg": "success",
              "bucket": dataType,
              "filepath": filepath
              }
        print(json)
        return json
    except Exception as ex:
        print(ex)
        return {"msg": "error"}


if __name__ == '__main__':
    main(sys.argv)
