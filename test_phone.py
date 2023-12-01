import pytest
import requests
from logger import Logger
from test_email import domain, user_agent

log_er = Logger("SoccerManager")
user_phone_num = "1234567890"


def send_verify_code_sms():
    """SMS Verify Code"""
    response = requests.post(url=domain + '/api/v1/player/login/sms-vc/send',
                             headers={'User-Agent': user_agent},
                             json={"telNo": user_phone_num})
    # response.raise_for_status()
    assert response.status_code == 200


def register_phone(first_name, last_name, password, verify_code):
    """Register with Phone Number"""
    response = requests.post(url=domain + '/api/v1/player/login/sms/register',
                             headers={'User-Agent': user_agent},
                             json={"firstName": first_name,
                                   "lastName": last_name,
                                   "pwd": password,
                                   "verifyCode": verify_code,
                                   "telNo": user_phone_num})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def login_phone(password):
    """Login with phone number."""
    response = requests.post(url=domain + '/api/v1/player/login/sms/login',
                             headers={'User-Agent': user_agent},
                             json={"pwd": password,
                                   "telNo": user_phone_num})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def reset_pwd_phone(password, verify_code):
    """Reset password using phone number. """
    response = requests.post(url=domain + "/api/v1/player/login/sms/reset-pwd",
                             headers={'User-Agent': user_agent},
                             json={"pwd": password,
                                   "verifyCode": verify_code,
                                   "telNo": user_phone_num})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200

