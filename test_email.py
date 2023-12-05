import pytest
import requests
from logger import Logger
import time

log_er = Logger("SoccerManager")
domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
valid_email = "muhsen@gmail.com"
valid_pwd = "password123"


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
            log_er.log_info(f" Verify Code for this email was already sent less than 5 minutes ago. Moving on to the"
                            f" next step.")
        else:
            log_er.log_info(f" Failed to obtain verify code: {response.json()}")
            vc_success = False
    return vc_success


def register_email(first_name, last_name, password, verify_code, email):
    response = requests.post(url=domain + '/api/v1/player/login/email/register',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={"firstName": first_name,
                                   "lastName": last_name,
                                   "pwd": password,
                                   "verifyCode": verify_code,
                                   "email": email})
    log_er.log_info(f" Registering player with following data: First Name: {first_name}, Last Name: {last_name}, "
                    f"Password: {password}, Verify Code: {verify_code}, Email: {email}")
    response_content = ""
    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
    else:
        response_content = response.json()  # gives error
    response_values = {"status_code": response.status_code, "response": response_content}
    return response_values


def login(phone="", email="", password=""):
    response = None
    if phone:
        response = requests.post(url=domain + '/api/v1/player/login/sms/login',
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password, "telNo": phone})
    elif email:
        response = requests.post(url=domain + '/api/v1/player/login/email/login',
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password, "email": email})

    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
        log_er.log_info(f" Login successful. Token: {response_content}")
    else:
        response_content = response.json()  # gives error
        log_er.log_info(f" Login failed. Error: {response_content}")
    return {"status_code": response.status_code, "response": response_content}


def reset_pwd(phone="", email="", password="", verify_code=""):
    response = None
    if phone:
        response = requests.post(url=domain + "/api/v1/player/login/sms/reset-pwd",
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password,
                                       "verifyCode": verify_code,
                                       "telNo": phone})
    elif email:
        response = requests.post(url=domain + "/api/v1/player/login/email/reset-pwd",
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password,
                                       "verifyCode": verify_code,
                                       "email": email})
    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
        log_er.log_info(f" Reset Password successful. Token: {response_content}")
    else:
        response_content = response.json()  # gives error
        log_er.log_info(f" Reset Password failed. Error: {response_content}")
    return {"status_code": response.status_code, "response": response_content}


def test_get_vc_valid_email():
    """ Get verify code with a valid email."""
    send_status = send_verify_code_email(valid_email)  # Does not return anything if success.
    assert send_status


def test_get_vc_invalid_email():
    """ Verify code should not be sent with an invalid email."""
    send_status = send_verify_code_email("muhsengmailcom")
    assert not send_status


def test_register_email_no_firstname():
    """Register email with no first name."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_email(valid_email)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="", last_name="Portman",
                                           password=valid_pwd, verify_code="6666", email=valid_email)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_lastname():
    """Register email with no last name."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_email(valid_email)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="Natalie", last_name="",
                                           password=valid_pwd, verify_code="6666", email=valid_email)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_pwd():
    """Register email with no password."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_email(valid_email)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="Natalie", last_name="Portman",
                                           password="", verify_code="6666", email=valid_email)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_vc():
    """Register email with no verify code."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_email(valid_email)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="Natalie", last_name="Portman",
                                           password=valid_pwd, verify_code="", email=valid_email)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_valid():
    """Register with valid email address and data."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_email(valid_email)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="Natalie", last_name="Portman",
                                           password=valid_pwd, verify_code="6666", email=valid_email)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


@pytest.mark.skip
def test_register_vc_within_5mins():
    """Verify code should NOT expire about 4.5 minutes after a verify code has been sent."""
    other_email = "readyplayerone@gmail.com"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(other_email)
    time.sleep(290)  # 4 minutes 50 seconds
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="Player", last_name="One",
                                           password="ReadyG0O", verify_code="6666", email=other_email)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


@pytest.mark.skip
def test_register_vc_more_than_5mins():
    """Verify code should expire 5 minutes after a verify code has been sent."""
    other_email = "playertwo@gmail.com"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(other_email)
    time.sleep(300)  # 5 minutes
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="Player", last_name="Two",
                                           password="ReadyG0O", verify_code="6666", email=other_email)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_wrong_verify_code():
    """Register email should be rejected if the wrong verify code is sent."""
    other_email = "player03@gmail.com"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(other_email)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_email(first_name="Player", last_name="Three",
                                           password="ReadyG0O", verify_code="1234", email=other_email)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Email\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Email Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_email_login():
    """Able to login using registered email and correct password."""
    login_response = login(email=valid_email, password=valid_pwd)
    assert login_response["status_code"] == 200


def test_email_login_wrong_pwd():
    """Unable to login using registered email but wrong password."""
    login_response = login(email=valid_email, password="password1234")
    if login_response["status_code"] == 400:
        error_json = login_response["response"]
        assert error_json['code'] == "PWD_IN_VALID"
    else:
        assert login_response["status_code"] == 400


def test_login_email_not_exists():
    """Unable to login using an email that is not registered yet."""
    login_response = login(email="mu@gmail.com", password=valid_pwd)
    if login_response["status_code"] == 400:
        error_json = login_response["response"]
        assert error_json['code'] == "EMAIL_NOT_EXISTS"
    else:
        assert login_response["status_code"] == 400


def test_reset_pwd_invalid_vc():
    """Unable to reset password with invalid verify code."""
    new_pwd = "321password"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(valid_email)
    # STEP 2 - Send a reset password request for a registered email.
    if vc_response:
        reset_pwd_response = reset_pwd(email=valid_email, password=new_pwd, verify_code="1234")
        if reset_pwd_response['status_code'] == 400:
            error_json = reset_pwd_response['response']
            assert error_json['code'] == "VC_NOT_VALID"
        else:
            assert reset_pwd_response['status_code'] == 400
    else:
        assert vc_response


def test_reset_pwd_valid_email():
    """Able to reset password with registered email."""
    new_pwd = "321password"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(valid_email)
    # STEP 2 - Send a reset password request for a registered email.
    if vc_response:
        reset_pwd_response = reset_pwd(email=valid_email, password=new_pwd, verify_code="6666")
        if reset_pwd_response["status_code"] == 200:
            login_response = login(email=valid_email, password=new_pwd)
            assert login_response["status_code"] == 200
        else:
            assert reset_pwd_response["status_code"] == 200
    else:
        assert vc_response


def test_reset_pwd_nonexist_email():
    """Unable to reset password with an email that is not registered yet."""
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email("unregistered@email.com")
    # STEP 2 - Send a reset password request for a registered email.
    time.sleep(1)
    if vc_response:
        reset_pwd_response = reset_pwd(email="unregistered@email.com", password=valid_pwd, verify_code="6666")
        if reset_pwd_response['status_code'] == 400:
            error_json = reset_pwd_response['response']
            assert error_json['code'] == "PLAYER_NOT_EXISTS"
        else:
            assert reset_pwd_response['status_code'] == 400
    else:
        assert vc_response
