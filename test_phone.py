import time
import requests
from test_email import domain, user_agent, log_er

user_phone_num = "1234567890"


def send_verify_code_sms(phone):
    response = requests.post(url=domain + '/api/v1/player/login/sms-vc/send',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={'telNo': phone})
    vc_success = True
    error = {}
    if response.status_code == 400:
        # As long as it does not return "vc not expired" error, continue.
        error = response.json()
        if error["code"] == "VC_NOT_EXPIRED":
            log_er.log_info(f" Verify Code for this phone number was already sent less than 5 minutes ago."
                            f" Moving on to the next step.")
        else:
            log_er.log_info(f" Failed to obtain verify code: {response.json()}")
            vc_success = False
    return vc_success


def register_phone(first_name, last_name, password, verify_code, phone_num):
    response = requests.post(url=domain + '/api/v1/player/login/sms/register',
                             headers={'Content-Type': 'application/json', 'User-Agent': user_agent},
                             json={"firstName": first_name,
                                   "lastName": last_name,
                                   "pwd": password,
                                   "verifyCode": verify_code,
                                   "telNo": phone_num})
    log_er.log_info(f" Registering player with following data: First Name: {first_name}, Last Name: {last_name}, "
                    f"Password: {password}, Verify Code: {verify_code}, Phone Number: {phone_num}")
    response_content = ""
    if response.status_code == 200:
        response_content = response.content.decode()  # gives token
    else:
        response_content = response.json()  # gives error
    response_values = {"status_code": response.status_code, "response": response_content}
    return response_values


def login_phone(password):
    response = requests.post(url=domain + '/api/v1/player/login/sms/login',
                             headers={'User-Agent': user_agent},
                             json={"pwd": password,
                                   "telNo": user_phone_num})
    return response.content.decode()


def reset_pwd_phone(password, verify_code):
    response = requests.post(url=domain + "/api/v1/player/login/sms/reset-pwd",
                             headers={'User-Agent': user_agent},
                             json={"pwd": password,
                                   "verifyCode": verify_code,
                                   "telNo": user_phone_num})
    return response.status_code


def test_get_vc_valid_phone():
    """ Get verify code with a valid phone number."""
    send_status = send_verify_code_sms(user_phone_num)  # Does not return anything if success.
    assert send_status


def test_get_vc_invalid_phone():
    """ Verify code should not be sent with an invalid phone number."""
    send_status = send_verify_code_sms("123456789")
    assert not send_status


def test_register_phone_no_firstname():
    """Register phone number with no first name."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(user_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="", last_name="Portman",
                                           password="Thor1234", verify_code="6666", phone_num=user_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_phone_no_lastname():
    """Register phone number with no last name."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(user_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Natalie", last_name="",
                                           password="Thor1234", verify_code="6666", phone_num=user_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_phone_no_pwd():
    """Register phone number with no password."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(user_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Natalie", last_name="Portman",
                                           password="", verify_code="6666", phone_num=user_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200 - This is a BUG.")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_email_no_vc():
    """Register phone number with no verify code."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(user_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Natalie", last_name="Portman",
                                           password="Thor1234", verify_code="", phone_num=user_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_register_phone_valid():
    """Register with valid email address and data."""
    # STEP 1 - Get Verify Code first
    vc_response = send_verify_code_sms(user_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Natalie", last_name="Portman",
                                           password="Thor1234", verify_code="6666", phone_num=user_phone_num)
        time.sleep(1)
        # STEP 3 - After register, get player info to verify data is correct.
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


def test_sms_vc_within_5mins():
    """Verify code should NOT expire about 4.5 minutes after a verify code has been sent to a phone number."""
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms("1991199119")
    time.sleep(285)  # 4 minutes 45 seconds
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Player", last_name="One",
                                           password="ReadyG0O", verify_code="6666", phone_num="1991199119")
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 200
    else:
        assert vc_response


def test_sms_vc_more_than_5mins():
    """Verify code should expire 5 minutes after a verify code has been sent to a phone number."""
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms("1551551551")
    time.sleep(30)  # 5 minutes
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Player", last_name="One",
                                           password="ReadyG0O", verify_code="6666", phone_num="1551551551")
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response


def test_wrong_sms_verify_code():
    """\'Register phone\' should be rejected if the wrong verify code is sent."""
    # STEP 1 - Get Verify Code
    vc_response = send_verify_code_sms(user_phone_num)
    time.sleep(1)
    # STEP 2 - Register with email. Success returns TOKEN.
    if vc_response:
        register_response = register_phone(first_name="Player", last_name="One",
                                           password="ReadyG0O", verify_code="1234", phone_num=user_phone_num)
        time.sleep(1)
        if register_response["status_code"] == 200:
            log_er.log_info(f"\'Register Phone\' Response Status Code: 200 - This is a Bug.")
        else:
            log_er.log_info(f" Register Phone Error: {register_response['response']}")
        assert register_response["status_code"] == 400
    else:
        assert vc_response
