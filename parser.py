import psycopg2
import requests
import json #библиотеки
import time

while (1):
    with open ('config.json', 'r', encoding='utf-8') as f: #открываем конфигурационный файл json
        text = json.load(f) # загнали все из файла в переменную

    for txt in text['owm']: # создали цикл, который будет работать построчно
        lat = (txt['lat']) # вытаскиваем переменные из файла
        lon = (txt['lon'])
        appid = (txt['appid'])

    try: # парсинг погоды
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params = {'lat': lat, 'lon':lon, 'units': 'metric', 'lang': 'eng', 'APPID': appid})
        data = res.json()
        coord_lat = data['coord']['lat']
        coord_lon = data['coord']['lon']
        unix_time = data['dt']
        temp = data['main']['temp']
        temp_feels = data['main']['feels_like']
        pressure = data['main']['pressure']
        pressure_sea = data['main']['sea_level']
        pressure_grnd = data['main']['grnd_level']
        humidity = data['main']['humidity']
        visibility = data['visibility']
        wind_seed = data['wind']['speed']
        wind_gust = data['wind']['gust']
        wind_deg = data['wind']['deg']
        clouds = data['clouds']['all']
        sunrise_unix = data['sys']["sunrise"]
        sunset_unix = data['sys']["sunset"]

    except:
        pass

    try:
        snow_1h = data['snow']['1h']
    except:
        snow_1h = 0
        pass

    try:
        rain_1h = data['rain']['1h']
    except:
        rain_1h = 0
        pass

    for txt in text['postgres']: # создали цикл, который будет работать построчно
        host = (txt['host'])
        user = (txt['user'])
        password = (txt['password'])
        database = (txt['database'])
        port = (txt['port'])

    connection = psycopg2.connect( # подключаемся к бд
        host = host,
        user = (user),
        password = (password),
        database = (database),
        port = (port)
        )
    print ("Database opened successfully")

    cur = connection.cursor()
    cur.execute(
        '''INSERT INTO owm_python_parser
        (coord_lat,coord_lon,unix_time,temp,temp_feels,
        pressure,pressure_sea,pressure_grnd,humidity,
        visibility,wind_seed,wind_gust,wind_deg,snow_1h,rain_1h,
        clouds,sunrise_unix,sunset_unix)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
        (coord_lat,coord_lon,unix_time,temp,temp_feels,
        pressure,pressure_sea,pressure_grnd,humidity,
        visibility,wind_seed,wind_gust,wind_deg,snow_1h,rain_1h,
        clouds,sunrise_unix,sunset_unix)
    )
    connection.commit()

    print ("Record inserted successfully")

    connection.close()
    time.sleep (3600)