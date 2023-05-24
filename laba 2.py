import requests
city = input ("Введите город: ")
APPID = "4fb71e5f047603d4d6d6278d45ce2ad4"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
             params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': APPID})
data = res.json()

print("Город:", city)
print("Погодные условия:", data['weather'][0]['description'])
print("Температура:", round(data['main']['temp']))
print("Минимальная температура:", round(data['main']['temp_min']))
print("Максимальная температура:", round(data['main']['temp_max']))
print("Скорость ветра", round(data['wind']['speed']))
print("Видимость", round(data['visibility']))

res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': APPID})
data = res.json()


print("Прогноз погоды на неделю:")
for i in data['list']:
    print("Дата <", i['dt_txt'], "> \r\nТемпература <", '{0:+3.0f}'.format(i['main']['temp']), "> \r\nПогодные условия <", i['weather'][0]['description'], "> \r\nСкорость ветра <", round(i['wind']['speed']), "> \r\nВидимость <", round(i['visibility']))
    print("____________________________")
