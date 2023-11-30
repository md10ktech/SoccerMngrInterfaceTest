import pytest
import requests
from logger import Logger
from test_email import domain, user_agent

log_er = Logger("SoccerManager")
user_phone_num = "1234567890"


def test_send_verify_code_sms():
    """SMS Verify Code"""
    response = requests.post(url=domain + '/api/v1/player/login/sms-vc/send',
                             headers={'User-Agent': user_agent},
                             json={"telNo": user_phone_num})
    # response.raise_for_status()
    assert response.status_code == 200


def test_register_phone():
    """Register with Phone Number"""
    response = requests.post(url=domain + '/api/v1/player/login/sms/register',
                             headers={'User-Agent': user_agent},
                             json={"firstName": "Denis",
                                   "lastName": "Bergkamp",
                                   "pwd": "1234qwer",
                                   "verifyCode": "6666",
                                   "telNo": user_phone_num})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_login_phone():
    """Login with phone number."""
    response = requests.post(url=domain + '/api/v1/player/login/sms/login',
                             headers={'User-Agent': user_agent},
                             json={"pwd": "1234qwer",
                                   "telNo": user_phone_num})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_reset_pwd_phone():
    """Reset password using phone number. """
    response = requests.post(url=domain + "/api/v1/player/login/sms/reset-pwd",
                             headers={'User-Agent': user_agent},
                             json={"pwd": "1234qwer",
                                   "verifyCode": "6666",
                                   "telNo": user_phone_num})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200

