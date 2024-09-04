import collections
import sys

import pandas as pd
import pymongo
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


def main(args):
    if 'pressure' in args:
        pressure = args['pressure']
    else:
        pressure = "1015"

    if 'humidity' in args:
        humidity = args['humidity']
    else:
        humidity = "70"

    return start(pressure, humidity)


mongoClient = pymongo.MongoClient('mongodb://mongo:27017/')
# mongoClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = mongoClient["smartCityDB"]
mycol = mydb["liveWeather"]


def start(pressure, humidity):
    try:
        return start_pre_process(pressure, humidity)
    except Exception as e:
        print(e)
        print("something went wrong")
        return {'error': "something went wrong"}


def start_pre_process(pressure, humidity):
    results = mycol.find({}, {'_id': False})

    weatherInfo = collections.defaultdict(list)

    for result in results:
        weatherInfo['temp'].append(float(result['main']['temp']))
        weatherInfo['feels_like'].append(float(result['main']['feels_like']))
        weatherInfo['pressure'].append(int(result['main']['pressure']))
        weatherInfo['humidity'].append(float(result['main']['humidity']))

    data = pd.DataFrame({
        'Humidity': weatherInfo['humidity'],
        'Pressure': weatherInfo['pressure'],
        'Temperature': weatherInfo['temp']
    })
    print(data.head())

    X = data[['Humidity', 'Pressure']]
    y = data['Temperature']
    return start_learning_more_methods(X, y, pressure, humidity)


def custom_score(mse, r2):
    normalized_mse = mse / 100
    normalized_r2 = r2 / 1
    return 1 * (-normalized_mse) + 1 * normalized_r2


def start_learning_more_methods(X, y, pressureLive, humidityLive):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(),
        "Support Vector Regressor": SVR(),
        "Gradient Boosting": GradientBoostingRegressor()
    }
    best_method = "none"
    previous_score = 0.0
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        score = custom_score(mse, r2)

        if previous_score < score:
            best_method = name
            previous_score = score

        print(name)
        print(f'Custom score: {score:.12f}°C')
        print("Mean Squared Error: " + str(mse))
        print("R-squared: " + str(r2))

        # # Plot the predictions vs the actual values
        # plt.scatter(y_test, y_pred, label=name)
        # plt.xlabel('Actual Temperature')
        # plt.ylabel('Predicted Temperature')
        # plt.title(f'{name} - Actual vs Predicted Temperature')
        # plt.legend()
        # plt.show()

    new_sample = [[humidityLive, pressureLive]]
    if best_method != "none":
        best_model = models.get(best_method)
        # best_model.fit(X_train, y_train)
        live_df = pd.DataFrame(new_sample, columns=['Humidity', 'Pressure'])
        predicted_temperature = best_model.predict(live_df)
        print(f'Prediction about humidity: {humidityLive} and pressure: {pressureLive}')
        print(f'Predicted Temperature ({best_method}): {predicted_temperature[0]:.2f}°C')
        return {'data': {
            'predicted_temperature': f'{predicted_temperature[0]:.2f}°C',
            'best_method': best_method
        }}
    else:
        print('Predicted Temperature failed')
        return "we had an issue, please try again"


if __name__ == '__main__':
    main(sys.argv)
