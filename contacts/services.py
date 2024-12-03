import requests
from loguru import logger


def send_email(recipient: str, subject: str, content: str) -> None: 
    url = 'https://sendemail.space/send-email/' 
    data = {
        'recipient': recipient, 
        'subject': subject, 
        'content': content,
    }

    response = requests.post(url, data=data)
    if not response.status_code == 200:
        logger.error(f'Ошибка при отправке email: {response.json()}')
    print('Отправка отработала')
