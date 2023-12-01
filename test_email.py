import requests
from logger import Logger
import time

log_er = Logger("SoccerManager")
domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
user_email = "muhsen@gmail.com"


def send_verify_code_email():
    response = requests.post(url=domain + '/api/v1/player/login/email-vc/send',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={'email': user_email})
    error = ""
    if not response.status_code == 200:
        error = response.json()
    response_values = {"status_code": response.status_code, "error": error}
    return response_values


def register_email(first_name, last_name, password, verify_code):
    response = requests.post(url=domain + '/api/v1/player/login/email/register',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={"firstName": first_name,
                                   "lastName": last_name,
                                   "pwd": password,
                                   "verifyCode": verify_code,
                                   "email": user_email})
    response_content = ""
    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
    else:
        response_content = response.json()  # gives error
    response_values = {"status_code": response.status_code, "response": response_content}
    return response_values


def login_email(password):
    response = requests.post(url=domain + '/api/v1/player/login/email/login',
                             headers={'User-Agent': user_agent},
                             json={"pwd": password,
                                   "email": user_email})
    return response.status_code


def reset_pwd_email(password, verify_code):
    response = requests.post(url=domain + "/api/v1/player/login/email/reset-pwd",
                             headers={'User-Agent': user_agent},
                             json={"pwd": password,
                                   "verifyCode": verify_code,
                                   "email": user_email})
    return response.status_code


def test_email_verify_code():
    """Able to obtain verify code for email address registration."""
    send_verify_code_email()


def test_register_email():
    """Register with valid email address."""
    # STEP 1 - Get Verify Code first
    verify_code_response = send_verify_code_email()
    time.sleep(1)
    if verify_code_response == 200:
        # STEP 2 - Register with email. Success returns TOKEN.
        register_response = register_email(first_name="Natalie", last_name="Portman",
                                           password="Thor1234", verify_code="6666")
        time.sleep(1)
        if register_response["status_code"] == 200:
            json_data = requests.get(url=domain + '/api/v1/player/info',
                                     headers={'User-Agent': user_agent, "Authorization": register_response["token"]})
            log_er.log_info(f" Player Info: {json_data}")
            assert register_response["status_code"] == 200
    else:
        log_er.log_info(f" Failed at obtaining verify code.")
        assert verify_code_response


# def test_template():
#     """Template"""
#     response = requests.put(url='https://soccer-manager-qa.qq72bian.com/api/v1/player/nickname',
#                             headers={'Authorization': token},
#                             params={'updateValue': 'Pele'})
#     if response.status_code == 200:
#         log_er.log_info(f" Token: {response.content.decode()} Timestamp: {datetime.now().strftime('%I:%M:%S%p')}")
#     else:
#         log_er.log_info(f" Response: {response.json()}")
#     log_er.log_info(f" Data: {response.json()}")
#     with open("api_data.json", mode="w") as data_file:
#         data_file.write(str(response.json()))
#     assert response.status_code == 200

