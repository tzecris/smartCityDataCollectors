import collections

import pandas as pd
import pymongo
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

def main():
    return start()


# mongoClient = pymongo.MongoClient('mongodb://mongo:27017/')
mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = mongoClient["smartCityDB"]
mycol = mydb["liveWeatherTest"]
mycol_avg = mydb["liveWeatherAvg"]


def start():
    try:
        return start_pre_process()
    except Exception as e:
        print(e)
        print("something went wrong")
        return {'error': "something went wrong"}


def start_pre_process():
    results = mycol.find({}, {'_id': False})

    weatherInfo = collections.defaultdict(list)

    for result in results:
        weatherInfo['temp'].append(float(result['temp']))
        weatherInfo['pressure'].append(int(result['sealevelpressure']))
        weatherInfo['humidity'].append(float(result['humidity']))
        weatherInfo['wind_speed'].append(float(result['windspeed']))

    data = pd.DataFrame({
        'humidity': weatherInfo['humidity'],
        'pressure': weatherInfo['pressure'],
        'temperature': weatherInfo['temp'],
        'wind_speed': weatherInfo['wind_speed']
    })
    print(data.head())

    features = ['temperature', 'humidity', 'wind_speed', 'pressure']
    data_scaled = StandardScaler().fit_transform(data[features])

    iso_forest = IsolationForest(contamination=0.01, random_state=42)
    data['anomaly'] = iso_forest.fit_predict(data_scaled)

    anomalies = data[data['anomaly'] == -1]

    plt.figure(figsize=(10,6))
    plt.plot(data.index, data['temperature'], label='Temperature', color='blue')
    plt.scatter(anomalies.index, anomalies['temperature'], color='red', label='Anomalies', marker='x')
    plt.title('Temperature with Anomalies Detected')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()
    plt.show()

    print("Number of anomalies detected: ", len(anomalies))
    print(anomalies)


if __name__ == '__main__':
    main()
