import requests
from logger import Logger
import time

log_er = Logger("SoccerManager")
domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
user_email = "muhsen@gmail.com"


def send_verify_code_email(email):
    response = requests.post(url=domain + '/api/v1/player/login/email-vc/send',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={'email': email})
    vc_success = True
    error = {}
    if response.status_code == 400:
        # As long as it does not return "vc not expired" error, continue.
        error = response.json()
        if error["code"] == "VC_NOT_EXPIRED":
            log_er.log_info(f" Verify Code for this email was already sent less than 5 minutes ago. Move on to the"
                            f" next step.")
        else:
            log_er.log_info(f" Failed to obtain verify code: {response.json()}")
            vc_success = False
    return vc_success


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
    return response.content.decode()


def reset_pwd_email(password, verify_code):
    response = requests.post(url=domain + "/api/v1/player/login/email/reset-pwd",
                             headers={'User-Agent': user_agent},
                             json={"pwd": password,
                                   "verifyCode": verify_code,
                                   "email": user_email})
    return response.status_code


def test_get_vc_valid_email():
    """ Get verify code with a valid email."""
    send_status = send_verify_code_email(user_email)  # Does not return anything if success.
    assert send_status


def test_get_vc_invalid_email():
    """ Verify code should not be sent with an invalid email."""
    send_status = send_verify_code_email("muhsengmailcom")
    assert not send_status


def test_register_email():
    """Register with valid email address. No standalone."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_email(user_email)
    time.sleep(1)
    if vc_response["status_code"] == 200:
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
        log_er.log_info(f" Failed obtaining verify code. Error: {vc_response['error']}")
        assert vc_response["status_code"]


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

