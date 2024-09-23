import requests
import sqlite3
import datetime

# Substitua 'YOUR_API_KEY' pela sua chave de API do OpenWeatherMap
API_KEY = 'API_KEY'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Conectar ao banco de dados SQLite (use o mesmo banco usado na consulta)
conn = sqlite3.connect('weather_forecast.db')  # Mudança aqui
c = conn.cursor()

# Criar tabela para armazenar as informações meteorológicas
c.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                temperature REAL,
                humidity INTEGER,
                description TEXT,
                datetime TEXT
            )''')
conn.commit()

# Função para obter dados da API do OpenWeatherMap
def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Para obter a temperatura em Celsius
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Função para salvar dados no banco de dados SQLite
def save_weather_data(city, temperature, humidity, description):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO weather_data (city, temperature, humidity, description, datetime) VALUES (?, ?, ?, ?, ?)",
              (city, temperature, humidity, description, now))
    conn.commit()

# Exemplo de uso
if __name__ == "__main__":
    # city = 'Batatais'
    city = 'Ribeirão Preto'
    data = get_weather_data(city)
    
    if data.get('cod') == 200:
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        
        save_weather_data(city, temperature, humidity, description)
        
        print(f"Dados salvos: {city} - Temp: {temperature}°C, Humidade: {humidity}%, Descrição: {description}")
    else:
        print("Cidade não encontrada!")

# Fechar conexão com o banco de dados
conn.close()
