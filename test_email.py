import pytest
import requests
from logger import Logger
import time
from random_email_mobile import randomize_email

log_er = Logger("SoccerManager")
domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
valid_email = randomize_email()
valid_pwd = "password123"
verify_code_const = "6666"


def send_verify_code_email(email):
    response = requests.post(url=domain + '/api/v1/player/login/email-vc/send',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={'email': email})
    log_er.log_info(f" -Sending verify code with email: {email}")
    vc_success = True
    error = {}
    if response.status_code == 400:
        # As long as it does not return "vc not expired" error, continue.
        error = response.json()
        if error["code"] == "VC_NOT_EXPIRED":
            log_er.log_info(f" -Verify Code for this email was already sent less than 5 minutes ago. Moving on to the"
                            f" next step.")
        else:
            log_er.log_info(f" -Failed to obtain verify code. Error: {response.json()}")
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
    log_er.log_info(f" -Registering player with following data: First Name= {first_name}, Last Name= {last_name}, "
                    f"Password= {password}, Verify Code= {verify_code}, Email= {email}")
    response_content = ""
    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
    else:
        response_content = response.json()  # gives error
        log_er.log_info(f" -Failed to register email. Error: {response_content}")
    response_values = {"status_code": response.status_code, "response": response_content}
    return response_values


def login(phone="", email="", password=""):
    response = None
    if phone:
        response = requests.post(url=domain + '/api/v1/player/login/sms/login',
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password, "telNo": phone})
        log_er.log_info(f" -Logging in with: Phone= {phone}, Password= {password}")
    elif email:
        response = requests.post(url=domain + '/api/v1/player/login/email/login',
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password, "email": email})
        log_er.log_info(f" -Logging in with: Email= {email}, Password= {password}")

    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
        log_er.log_info(f" -Login successful.")
    else:
        response_content = response.json()  # gives error
        log_er.log_info(f" -Login failed. Error: {response_content}")
    return {"status_code": response.status_code, "response": response_content}


def validate_email_pwd(email="muhsen@gmail.com", pwd="Password123"):
    response = requests.post(url=domain + '/api/v1/player/login/email-pwd/verify',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={"pwd": pwd, 'email': email})
    log_er.log_info(f" -Validating email: {email} and password: {pwd}")
    verify_success = True
    if response.status_code == 400:
        # As long as it does not return "vc not expired" error, continue.
        error = response.json()
        log_er.log_info(f" -Failed to validate input: {response.json()}")
        verify_success = False
    return verify_success


def reset_pwd(phone="", email="", password="", temp_token=""):
    response = None
    if phone:
        response = requests.post(url=domain + "/api/v1/player/login/sms/reset-pwd",
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password,
                                       "tmpToken": temp_token,
                                       "telNo": phone})
    elif email:
        response = requests.post(url=domain + "/api/v1/player/login/email/reset-pwd",
                                 headers={'User-Agent': user_agent},
                                 json={"pwd": password,
                                       "tmpToken": temp_token,
                                       "email": email})
    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
        log_er.log_info(f" -Reset Password successful.")
    else:
        response_content = response.json()  # gives error
        log_er.log_info(f" -Reset Password failed. Error: {response_content}")
    return {"status_code": response.status_code, "response": response_content}


def get_temp_token(email):
    response = requests.post(url=domain + "/api/v1/player/login/email/verify-vc",
                             headers={'User-Agent': user_agent},
                             json={"verifyCode": verify_code_const,
                                   "email": email})
    return response.content.decode()

# -------------------- TEST FUNCTIONS -------------------- #


def test_get_vc_valid_email():
    """Able to get verify code with a valid email."""
    send_status = send_verify_code_email(valid_email)  # Does not return anything if success.
    assert send_status


def test_get_vc_invalid_email():
    """Unable to get verify code with an invalid email."""
    send_status = send_verify_code_email("muhsengmailcom")
    assert not send_status


def test_register_email_no_firstname():
    """Unable to register email with no first name."""
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
            log_er.log_info(f" -\'Register Email\' status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_lastname():
    """Unable to register email with no last name."""
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
            log_er.log_info(f" -\'Register Email\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_pwd():
    """Unable to register email with no password."""
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
            log_er.log_info(f" -\'Register Email\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_vc():
    """Unable to register email with no verify code."""
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
            log_er.log_info(f" -\'Register Email\' status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_valid():
    """Able to register with valid email address and data."""
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
            log_er.log_info(f" -\'Register Email\' Response Status Code: 200")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


@pytest.mark.skip
def test_register_vc_within_5mins():
    """Verify code should NOT expire 4.75 minutes after a verify code has been sent."""
    other_email = "readyplayerone@gmail.com"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(other_email)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        time.sleep(290)  # 4 minutes 50 seconds
        log_er.log_info(f" -Waiting for 4 minutes and 50 seconds to pass.")
        register_response = register_email(first_name="Player", last_name="One",
                                           password="ReadyG0O", verify_code="6666", email=other_email)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Email\' Response Status Code: 200")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


@pytest.mark.skip
def test_register_vc_more_than_5mins():
    """Verify code should expire 5 minutes after a verify code has been sent."""
    other_email = "playertwo@gmail.com"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(other_email)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        time.sleep(300)  # 5 minutes
        log_er.log_info(f" -Waiting for 5 minutes to pass.")
        register_response = register_email(first_name="Player", last_name="Two",
                                           password="ReadyG0O", verify_code="6666", email=other_email)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Email\' status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_wrong_verify_code():
    """Register email should be rejected if the wrong verify code is passed in."""
    other_email = "player03@gmail.com"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(other_email)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        log_er.log_info(f" -Non-existent Verify Code= \"1234\"")
        register_response = register_email(first_name="Player", last_name="Three",
                                           password="ReadyG0O", verify_code="1234", email=other_email)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Email\' status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_email_login():
    """Able to login using registered email and correct password."""
    login_response = login(email=valid_email, password=valid_pwd)
    log_er.log_info(f" -Email= {valid_email}, Password= {valid_pwd}")
    assert login_response["status_code"] == 200


def test_email_login_wrong_pwd():
    """Unable to login using registered email but wrong password."""
    login_response = login(email=valid_email, password="password1234")
    log_er.log_info(f" -Password= \"password1234\"")
    if login_response["status_code"] == 400:
        error_json = login_response["response"]
        assert error_json['code'] == "PWD_IN_VALID"
    else:
        assert login_response["status_code"] == 400


def test_login_email_not_exists():
    """Unable to login using an email that is not registered yet."""
    login_response = login(email="this_emaiL_does_not_exist@nomail.com", password=valid_pwd)
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
        reset_pwd_response = reset_pwd(email=valid_email, password=new_pwd, temp_token="1234")
        log_er.log_info(f" -New Password= {new_pwd}, Token= \"1234\"")
        if reset_pwd_response['status_code'] == 400:
            error_json = reset_pwd_response['response']
            assert error_json['code'] == "PARAMETER_INVALID"
        else:
            assert reset_pwd_response['status_code'] == 400
    else:
        assert vc_response


def test_reset_pwd_valid_email():
    """Able to reset password with registered email."""
    new_pwd = "321password"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(valid_email)
    # STEP 2 - Get Temp Token
    temp_token = get_temp_token(valid_email)
    # STEP 3 - Send a reset password request for a registered email.
    if vc_response:
        log_er.log_info(f" -New Password= {new_pwd}")
        reset_pwd_response = reset_pwd(email=valid_email, password=new_pwd, temp_token=temp_token)
        # STEP 4 - Try to login with new password.
        if reset_pwd_response["status_code"] == 200:
            login_response = login(email=valid_email, password=new_pwd)
            assert login_response["status_code"] == 200
        else:
            assert reset_pwd_response["status_code"] == 200
    else:
        assert vc_response


def test_reset_pwd_nonexist_email():
    """Unable to reset password with an email that is not registered yet."""
    unreg_email = "unregistered@nomail.com"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_email(unreg_email)
    # STEP 3 - Get Temp Token
    temp_token = get_temp_token(unreg_email)
    # STEP 2 - Send a reset password request for a registered email.
    time.sleep(1)
    if vc_response:
        reset_pwd_response = reset_pwd(email=unreg_email, password=valid_pwd, temp_token=temp_token)
        if reset_pwd_response['status_code'] == 400:
            error_json = reset_pwd_response['response']
            assert error_json['code'] == "PLAYER_NOT_EXISTS"
        else:
            assert reset_pwd_response['status_code'] == 400
    else:
        assert vc_response


def test_validate_email_success():
    """Valid email and password should return success."""
    assert validate_email_pwd(email=randomize_email())


def test_validate_email_fail():
    """Verify invalid email only, and invalid password only, and both."""
    fail = 0
    # validate email format.
    if not validate_email_pwd("not@email", "Password123"):
        fail += 1
    # validate if email is already registered.
    if not validate_email_pwd(email="muhsen@gmail.com", pwd="Password123"):
        fail += 1
    # validate if password meets requirement.
    if not validate_email_pwd(randomize_email(), "password123"):
        fail += 1

    log_er.log_info(f" Num of Failed Validation: {fail}")
    assert fail == 3
