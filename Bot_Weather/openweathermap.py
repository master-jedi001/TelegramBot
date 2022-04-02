import requests
import config


class Weather:
    base_url = 'https://api.openweathermap.org/data/2.5/weather'

    def __init__(self, city):
        self.city = city
        self.temp = None
        self.desc = None

    def __str__(self):
        return f'Погода в городе {self.city}\nТемпература: {self.temp} °C\n{self.desc}'

    def get(self, language):
        try:
            data = requests.get(
                Weather.base_url,
                params={
                    'q': self.city,
                    'units': 'metric',
                    'lang': language,
                    'appid': config.weather_token
                }).json()

            self.desc = data['weather'][0]['description']
            self.temp = int(data['main']['temp'])
            return self
        except Exception:
            return 'Не найден город, попробуйте ввести название снова.'
