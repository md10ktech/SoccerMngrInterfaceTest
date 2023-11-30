import pytest
import requests
from logger import Logger

log_er = Logger("SoccerManager")
domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
user_email = "muhsen@gmail.com"


def test_send_verify_code_email():
    """Send Verify Code via email"""
    response = requests.post(url=domain + '/api/v1/player/login/email-vc/send',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={'email': user_email})
    # returns nothing
    assert response.status_code == 200


def test_register_email():
    """Register with email address"""
    response = requests.post(url=domain + '/api/v1/player/login/email/register',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={"firstName": "M",
                                   "lastName": "D",
                                   "pwd": "password123",
                                   "verifyCode": "1234",
                                   "email": user_email})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_login_email():
    """Login with email address."""
    response = requests.post(url=domain + '/api/v1/player/login/email/login',
                             headers={'User-Agent': user_agent},
                             json={"pwd": "password123",
                                   "email": user_email})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_reset_pwd_email():
    """Reset password using email address. """
    response = requests.post(url=domain + "/api/v1/player/login/email/reset-pwd",
                             headers={'User-Agent': user_agent},
                             json={"pwd": "password123",
                                   "verifyCode": "6666",
                                   "email": user_email})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


# def test_template():
#     """Template"""
#     response = requests.put(url='https://soccer-manager-qa.qq72bian.com/api/v1/player/nickname',
#                             headers={'Authorization': token},
#                             params={'updateValue': 'Pele'})
#     log_er.log_info(f" Data: {response.json()}")
#     with open("api_data.json", mode="w") as data_file:
#         data_file.write(str(response.json()))
#     assert response.status_code == 200

