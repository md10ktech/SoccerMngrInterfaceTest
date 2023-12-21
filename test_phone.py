import time

import pytest
import requests
from test_email import domain, user_agent, log_er, login, reset_pwd
from random_email_mobile import randomize_mobile_num

valid_phone_num = randomize_mobile_num()
valid_password = "Password123"
verify_code_const = "6666"


def send_verify_code_sms(phone):
    response = requests.post(url=domain + '/api/v1/player/login/sms-vc/send',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={'telNo': phone})
    log_er.log_info(f" -Sending verify code with phone number: {phone}")
    vc_success = True
    error = {}
    if response.status_code == 400:
        # As long as it does not return "vc not expired" error, continue.
        error = response.json()
        if error["code"] == "VC_NOT_EXPIRED":
            log_er.log_info(f" -Verify Code for this phone number was already sent less than 5 minutes ago."
                            f" Moving on to the next step.")
        else:
            log_er.log_info(f" -Failed to obtain verify code: {response.json()}")
            vc_success = False
    return vc_success


def validate_phone_pwd(phone="1234568790", pwd="Password123"):
    response = requests.post(url=domain + '/api/v1/player/login/mobile-pwd/verify',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={"pwd": pwd, 'telNo': phone})
    log_er.log_info(f" -Validating phone number: {phone} and password: {pwd}")
    verify_success = True
    if response.status_code == 400:
        # As long as it does not return "vc not expired" error, continue.
        error = response.json()
        log_er.log_info(f" -Failed to verify input: {response.json()}")
        verify_success = False
    return verify_success


def register_phone(first_name, last_name, password, verify_code, phone_num):
    response = requests.post(url=domain + '/api/v1/player/login/sms/register',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={"firstName": first_name,
                                   "lastName": last_name,
                                   "pwd": password,
                                   "verifyCode": verify_code,
                                   "telNo": phone_num})
    log_er.log_info(f" -Registering player with following data: First Name: {first_name}, Last Name: {last_name}, "
                    f"Password: {password}, Verify Code: {verify_code}, Phone Number: {phone_num}")
    response_content = ""
    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
    else:
        response_content = response.json()  # gives error
        log_er.log_info(f" -Failed to register phone number. Error: {response_content}")
    response_values = {"status_code": response.status_code, "response": response_content}
    return response_values


def get_temp_token(email):
    response = requests.post(url=domain + "/api/v1/player/login/email/verify-vc",
                             headers={'User-Agent': user_agent},
                             json={"verifyCode": verify_code_const,
                                   "email": email})
    return response.content.decode()

# -------------------- TEST FUNCTIONS -------------------- #


def test_get_vc_valid_phone():
    """ Get verify code with a valid phone number."""
    send_status = send_verify_code_sms(valid_phone_num)  # Does not return anything if success.
    assert send_status


def test_get_vc_invalid_phone_too_short():
    """ Verify code should not be sent with an invalid phone number."""
    send_status = send_verify_code_sms("123456789")
    assert not send_status


def test_get_vc_invalid_country_code():
    """ Verify code should not be sent with an invalid phone number."""
    send_status = send_verify_code_sms("99934567890234")
    assert not send_status


def test_register_phone_no_firstname():
    """Register phone number with no first name."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(valid_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="", last_name="Theron",
                                           password=valid_password, verify_code="6666", phone_num=valid_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_phone_no_lastname():
    """Register phone number with no last name."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(valid_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Charlize", last_name="",
                                           password=valid_password, verify_code="6666", phone_num=valid_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_phone_no_pwd():
    """Register phone number with no password."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(valid_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Charlize", last_name="Theron",
                                           password="", verify_code="6666", phone_num=valid_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_vc():
    """Register phone number with no verify code."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(valid_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Charlize", last_name="Theron",
                                           password=valid_password, verify_code="", phone_num=valid_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_phone_valid():
    """Register with valid email address and data."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(valid_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Natalie", last_name="Portman",
                                           password=valid_password, verify_code="6666", phone_num=valid_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


@pytest.mark.skip
def test_sms_vc_within_5mins():
    """Verify code should NOT expire about 4.5 minutes after a verify code has been sent to a phone number."""
    other_phone = "1201001001"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(other_phone)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        time.sleep(290)  # 4 minutes 45 seconds
        log_er.log_info(f" -Waiting for 4 minutes 45 seconds to pass.")
        register_response = register_phone(first_name="Player", last_name="One",
                                           password="ReadyG0O", verify_code="6666", phone_num=other_phone)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


@pytest.mark.skip
def test_sms_vc_more_than_5mins():
    """Verify code should expire 5 minutes after a verify code has been sent to a phone number."""
    other_phone = "1214161810"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(other_phone)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        time.sleep(300)  # 5 minutes
        log_er.log_info(f" -Waiting for 5 minutes to pass.")
        register_response = register_phone(first_name="Player", last_name="One",
                                           password="ReadyG0O", verify_code="6666", phone_num=other_phone)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_sms_wrong_verify_code():
    """\'Register phone\' should be rejected if the wrong verify code is sent."""
    other_phone = "1231231231"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(other_phone)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        log_er.log_info(f" -Non-existent Verify Code= \"1234\"")
        register_response = register_phone(first_name="Player", last_name="Three",
                                           password="ReadyG0O", verify_code="1234", phone_num=other_phone)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f" -\'Register Phone\' Response Status Code: 200. Bug!")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_phone_login():
    """Able to login using registered phone number and correct password."""
    login_response = login(phone=valid_phone_num, password=valid_password)
    log_er.log_info(f" -Phone Number= {valid_phone_num}, Password= {valid_password}")
    assert login_response["status_code"] == 200


def test_phone_login_wrong_pwd():
    """Unable to login using registered phone number but wrong password."""
    login_response = login(phone=valid_phone_num, password="password1234")
    log_er.log_info(f" -Password= \"password1234\"")
    if login_response["status_code"] == 400:
        error_json = login_response["response"]
        assert error_json['code'] == "PWD_IN_VALID"
    else:
        assert login_response["status_code"] == 400


def test_login_phone_not_exists():
    """Unable to login using registered phone number but wrong password."""
    login_response = login(phone="1236547899", password=valid_password)
    log_er.log_info(f" -Non-existent Phone Number= \"1236547899\"")
    if login_response["status_code"] == 400:
        error_json = login_response["response"]
        assert error_json['code'] == "MOBILE_NUMBER_NOT_EXISTS"
    else:
        assert login_response["status_code"] == 400


def test_reset_pwd_invalid_vc():
    """Unable to reset password with invalid verify code."""
    new_pwd = "PassTheWord"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(valid_phone_num)
    # STEP 2 - Send a reset password request for a registered email.
    if vc_response:
        reset_pwd_response = reset_pwd(phone=valid_phone_num, password=new_pwd, temp_token="1234")
        log_er.log_info(f" -New Password= {new_pwd}, VC= \"1234\"")
        if reset_pwd_response['status_code'] == 400:
            error_json = reset_pwd_response['response']
            assert error_json['code'] == "VC_NOT_VALID"
        else:
            assert reset_pwd_response['status_code'] == 400
    else:
        assert vc_response


def test_reset_pwd_valid_phone():
    """Able to reset password with registered phone number."""
    new_pwd = "PassTheWord"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(valid_phone_num)
    # STEP 2 - Send a reset password request for a registered phone number.
    if vc_response:
        log_er.log_info(f" -New Password= {new_pwd}")
        reset_pwd_response = reset_pwd(phone=valid_phone_num, password=new_pwd, temp_token="6666")
        # STEP 3 - Try to login with new password.
        if reset_pwd_response["status_code"] == 200:
            login_response = login(phone=valid_phone_num, password=new_pwd)
            assert login_response["status_code"] == 200
        else:
            assert reset_pwd_response["status_code"] == 200
    else:
        assert vc_response


def test_reset_pwd_nonexist_phone():
    """Unable to reset password with an email that is not registered yet."""
    nonexistent_phone = "1232587891"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(nonexistent_phone)
    # STEP 2 - Send a reset password request for a registered email.
    time.sleep(1)
    if vc_response:
        reset_pwd_response = reset_pwd(phone=nonexistent_phone, password="321password", temp_token="6666")
        if reset_pwd_response['status_code'] == 400:
            error_json = reset_pwd_response['response']
            assert error_json['code'] == "PLAYER_NOT_EXISTS"
        else:
            assert reset_pwd_response['status_code'] == 400
    else:
        assert vc_response


def test_verify_phone_pwd():
    """Able to verify phone and password in login."""
    nonexistent_phone = "1232587890"
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(nonexistent_phone)
    # STEP 2 - Send a reset password request for a registered email.
    time.sleep(1)
    if vc_response:
        reset_pwd_response = reset_pwd(phone=nonexistent_phone, password="321password", temp_token="6666")
        if reset_pwd_response['status_code'] == 400:
            error_json = reset_pwd_response['response']
            assert error_json['code'] == "PLAYER_NOT_EXISTS"
        else:
            assert reset_pwd_response['status_code'] == 400
    else:
        assert vc_response


def test_verify_phone_success():
    """Verify valid phone and password"""
    assert validate_phone_pwd("3216549870", "password123")


def test_verify_phone_fail():
    """Verify invalid phone only, and invalid password only, and both."""
    fail = 0
    if validate_phone_pwd("321654987", "Password123"):
        fail += 1
    if validate_phone_pwd("3216549807", "123"):
        fail += 1
    if validate_phone_pwd("321654987", "password123"):
        fail += 1

    log_er.log_info(f" Verified OK: {fail}")
    assert fail == 3



