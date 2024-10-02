import pandas as pd
import numpy as np
import collections

import pymongo
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = mongoClient["smartCityDB"]
mycol = mydb["liveWeatherTest"]
mycol_avg = mydb["liveWeatherAvg"]

def start_process():
    results = mycol.find({}, {'_id': False})

    weatherInfo = collections.defaultdict(list)

    for result in results:
        weatherInfo['temp'].append(float(result['temp']))
        weatherInfo['pressure'].append(int(result['sealevelpressure']))
        weatherInfo['humidity'].append(float(result['humidity']))
        weatherInfo['wind_speed'].append(float(result['windspeed']))

    data = pd.DataFrame({
        'humidity': weatherInfo['humidity'],
        # 'pressure': weatherInfo['pressure'],
        # 'temperature': weatherInfo['temp'],
        'wind_speed': weatherInfo['wind_speed']
    })
    print(data.head())
    df = pd.DataFrame(data)

    scaler = StandardScaler()
    # features = ['temperature', 'humidity', 'wind_speed', 'pressure']
    data_scaled = scaler.fit_transform(df)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(data_scaled)

    # DBSCAN
    # dbscan = DBSCAN(eps=0.5, min_samples=2)
    # df['cluster'] = dbscan.fit_predict(data_scaled)

    # plt.figure(figsize=(10, 7))
    # plt.scatter(df['temperature'], df['humidity'], c=df['cluster'], cmap='viridis')
    # plt.title('Clustering Weather Data (Temperature vs Humidity)')
    # plt.xlabel('Temperature (°C)')
    # plt.ylabel('Humidity (%)')
    # plt.colorbar(label='Cluster')
    # plt.show()

    plt.figure(figsize=(10, 7))
    plt.scatter(df['wind_speed'], df['humidity'], c=df['cluster'], cmap='viridis')
    plt.title('Clustering Weather Data (Wind Speed vs Humidity)')
    plt.xlabel('Wind speed')
    plt.ylabel('Humidity (%)')
    plt.colorbar(label='Cluster')
    plt.show()

    # plt.figure(figsize=(10, 7))
    # plt.scatter(df['temperature'], df['pressure'], c=df['cluster'], cmap='viridis')
    # plt.title('Clustering Weather Data (Temperature vs Pressure)')
    # plt.xlabel('Temperature (°C)')
    # plt.ylabel('Pressure')
    # plt.colorbar(label='Cluster')
    # plt.show()

    # plt.figure(figsize=(10, 7))
    # plt.scatter(df['temperature'], df['wind_speed'], c=df['cluster'], cmap='viridis')
    # plt.title('Clustering Weather Data (Temperature vs Wind Speed)')
    # plt.xlabel('Temperature (°C)')
    # plt.ylabel('Wind speed')
    # plt.colorbar(label='Cluster')
    # plt.show()

    real_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    print("\nCluster Centers (Real Values):")
    print(real_centers)


if __name__ == '__main__':
    start_process()
