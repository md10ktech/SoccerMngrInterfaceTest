import requests
from test_email import domain, user_agent, register_email, send_verify_code_email, log_er, login_email, user_email
from test_phone import register_phone, send_verify_code_sms

# Test inputs
password = "password123"


def get_player_info(register_token):  # Passing in token here to prevent scope issues
    if register_token:
        response = requests.get(url=domain + '/api/v1/player/info',
                                headers={'User-Agent': user_agent, 'Authorization': register_token})
        log_er.log_info(f" Get Player Info Data: {response.json()}")
        # response.raise_for_status()
        return response.json()
    else:
        return "No json obtained."


def test_get_player_info_email():
    """Able to get Player Info of user who registered with email."""
    # Step 1 : Send verify code first.
    verify_code_response = send_verify_code_email(user_email)
    if not verify_code_response:
        assert verify_code_response
    # Step 2 : Register with email (global variable in test_email.py)
    register_response = register_email(first_name="Natalie", last_name="Portman",
                                       password=password, verify_code="6666")
    # Step 3 : Obtained token to be used for getting player info
    if register_response["status_code"] == 200:
        token = register_response["response"]
        log_er.log_info(f" Data: {get_player_info(token)}")
    else:
        log_er.log_info(f" Failed to register with email: {register_response['response']}")
    assert register_response["status_code"] == 200


def test_get_player_info_phone():
    """Able to get Player Info of user who registered with phone number."""
    # Step 1 : Send verify code first.
    verify_code_response = send_verify_code_sms()
    if verify_code_response['status_code'] == 400:
        # As long as it does not return "vc not expired" error, continue to Step 2 and 3.
        if verify_code_response['error']["code"] == "VC_NOT_EXPIRED":
            log_er.log_info(f" Verify Code for this phone number was just sent less than 5 minutes ago.")
        else:
            log_er.log_info(f" Failed to obtain verify code: {verify_code_response['error']}")
            assert verify_code_response['status_code'] == 200
    # Step 2 : Register with email (global variable in test_email.py)
    register_response = register_phone(first_name="Natalie", last_name="Portman",
                                       password="Thor1234", verify_code="6666")
    # Step 3 : Obtained token to be used for getting player info
    if register_response["status_code"] == 200:
        phone_token = register_response["response"]
        log_er.log_info(f" Data: {get_player_info(phone_token)}")
    else:
        log_er.log_info(f" Failed to register with phone number: {register_response['response']}")
    assert register_response["status_code"] == 200


def test_update_nickname():
    """Able to change nickname of a player."""
    token = login_email(password)
    response = requests.put(url=domain + "/api/v1/player/nickname",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            json={"updateValue": "Luke Skywalker"})
    if response.status_code == 200:
        log_er.log_info(f" Nickname successfully changed. Updated Player Info: {get_player_info(token)}")
    else:
        log_er.log_info(f" Error: {response.json()}")
    assert response.status_code == 200


def test_update_club_name():
    """Able to change club name."""
    token = login_email(password)
    response = requests.put(url=domain + "/api/v1/player/club-name",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            json={"updateValue": "Black Pink Fan Club"})
    if response.status_code == 200:
        log_er.log_info(f" Club Name successfully changed. Updated Player Info: {get_player_info(token)}")
    else:
        log_er.log_info(f" Error: {response.json()}")
    assert response.status_code == 200


def test_update_head_icon_index():
    """Able to change nickname of a player"""
    token = login_email(password)
    response = requests.put(url=domain + "/api/v1/player/head-icon",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            json={"updateValue": "7e53nt"})
    if response.status_code == 200:
        log_er.log_info(f" Head Icon index successfully changed. Updated Player Info: {get_player_info(token)}")
    else:
        log_er.log_info(f" Error: {response.json()}")
    assert response.status_code == 200


def test_get_generated_name():
    """Able to change nickname of a player"""
    token = login_email(password)
    response = requests.get(url=domain + "/api/v1/player/system-generated-name",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            params={"player-name-type": "NICK_NAME"})
    if response.status_code == 200:
        log_er.log_info(f" Name successfully generated. Provided name: {response.content.decode()}")
    else:
        log_er.log_info(f" Error: {response.json()}")
    assert response.status_code == 200
