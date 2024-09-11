import requests
import sys

def get_notifications(lat, lon):

    api_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,rain_sum,snowfall_sum,wind_speed_10m_max"
    }
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()

        daily_weather = data.get('daily', {})
        dates = daily_weather.get('time', [])
        max_temps = daily_weather.get('temperature_2m_max', [])
        min_temps = daily_weather.get('temperature_2m_min', [])
        rain_sum = daily_weather.get('rain_sum', [])
        wind_speed_max = daily_weather.get('wind_speed_10m_max', [])

        def has_bad_weather(max_temp, min_temp, rain, wind_speed):
            reasons = []
            if max_temp > 30:
                reasons.append(f"high temperatures, around {max_temp} C")
            if min_temp < 5:
                reasons.append(f"low temperatures, around {min_temp} C")
            if rain > 10:
                reasons.append(f"high amount of rain, around {rain} mm")
            if wind_speed > 15:
                reasons.append(f"high wind speeds, {wind_speed} km/h")
            return reasons


        weather_report = []
        for i in range(len(dates)):
            reasons = has_bad_weather(max_temps[i], min_temps[i], rain_sum[i], wind_speed_max[i])
            weather_report.append({
                "date": dates[i],
                "max_temp": max_temps[i],
                "min_temp": min_temps[i],
                "rain_sum": rain_sum[i],
                "wind_speed_max": wind_speed_max[i],
                "bad_weather": reasons
            })


        print("Weather Report for the Next Days:")
        for report in weather_report:
            if report['bad_weather']:
                print(f"Date: {report['date']}")
                print(f"  Max Temp: {report['max_temp']}°C")
                print(f"  Min Temp: {report['min_temp']}°C")
                print(f"  Rain Sum: {report['rain_sum']} mm")
                print(f"  Max Wind Speed: {report['wind_speed_max']} km/h")
                for reason in report['bad_weather']:
                    print(f" Reason: {reason}")

        return {'data': weather_report}
    else:
        return {'error': 'Something went wrong'}


def main(args):
    if 'lat' in args:
        lat = args['lat']
    else:
        lat = 37.9756
    if 'lon' in args:
        lon = args['lon']
    else:
        lon = 23.7348

    return get_notifications(lat, lon)


if __name__ == '__main__':
    main(sys.argv)
