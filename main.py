import logging

import requests
from bs4 import BeautifulSoup as bs

import config


def send_verification_code(phone_number: int) -> str:
    """
    Send verification code to phone number
    
    :param phone_number: The phone number you want to send the code to
    :type phone_number: int
    :return: A token
    """
    data = '{"username":"%s"}' % (phone_number)

    response = requests.post(
        'https://www.sheypoor.com/api/v10.0.0/auth/send',
        headers=config.authenticate_headers,
        data=data
    )
    return response.json()['data']['verify']['token']


def authenticate(verify_token: int, verification_code: int) -> dict:
    """
    It takes a phone number and a verification code and returns a token.
    Authenticate 
    
    :param phone_number: The phone number you want to send the verification code to
    :type phone_number: int
    :param verification_code: The code you received from the SMS
    :type verification_code: int
    :return: A dictionary
    """
    data = {
        'verify_token': verify_token,
        'verification_code': verification_code,
    }
    response = requests.post(
        'https://www.sheypoor.com/api/v10.0.0/auth/verify',
        headers=config.authenticate_headers,
        json=data
    )
    return response.json()


def get_ads(last_page: int) -> list:
    ads = []
    for page in range(1, last_page):
        url = f'https://www.sheypoor.com/اصفهان/املاک/رهن-اجاره-خانه-آپارتمان?p={page}'
        response = requests.get(url, headers=config.headers)
        soup = bs(response.text, 'html.parser')
        ads.extend(
            ad['href'].split("-")[-1].split(".html")[0] for ad in soup.select('#serp .content a')
        )
        logging.info(f'Page {page} Scraped.')


def get_number(ad_id: int) -> str:
    response = requests.get(
        f'https://www.sheypoor.com/api/web/listings/{ad_id}/number',
        cookies=config.cookies,
        headers=config.headers,
    )
    return response.json()['data']['mobileNumber']


# Configure logging
logging.basicConfig(level=logging.INFO)
