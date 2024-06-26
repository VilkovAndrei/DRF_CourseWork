import requests


def send_message_to_tg(token, chat_id, message):  # Функция интеграции с Телеграмм
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.get(url, data=data)
    return response.json()
