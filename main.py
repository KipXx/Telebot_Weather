import telebot
import requests
import json

bot = telebot.TeleBot('5946513884:AAGkl2MPaJ5sK0BRYsbWkY6PV23JJBF1-aU')
API = '709e3cbe105d05f7bfdb27403929d3bc'

weather_mapping = {
    'clear sky': 'ясно',
    'few clouds': 'мало облаков',
    'scattered clouds': 'рассеянные облака',
    'overcast clouds': 'затянуто облаками',
    'broken clouds': 'облачно',
    'shower rain': 'ливень',
    'rain': 'дождь',
    'thunderstorm': 'гроза',
    'snow': 'снег',
    'mist': 'туман',
}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Какого города вы хотите узнать погоду?')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_description_en = data["weather"][0]["description"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]

        weather_description_ru = weather_mapping.get(weather_description_en, weather_description_en)

        # Создаем строку с подробной информацией о погоде
        weather_info = f'🌤️Сейчас погода: {weather_description_ru}\n🌡️Температура: {temp}°C\n🤲Ощущается как: {feels_like}°C\n🎈Давление: {pressure} мбар\n🍃Скорость ветра: {wind_speed} м/с'
        image = 'sun.png' if temp > 15.0 else 'cloud.png'
        with open(image, 'rb') as file:
            bot.send_photo(message.chat.id, file, caption=weather_info)
    else:
        bot.reply_to(message, f'Город указан неверно или я такой не знаю... 🥺')

bot.polling(none_stop=True)
