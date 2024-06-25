import requests
from settings import TELEGRAM_API_URL

def send_message_to_tg(token, chat_id, message):  # Функция интеграции с Телеграмм
    url = f"{TELEGRAM_API_URL}{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.get(url, data=data)
    return response.json()