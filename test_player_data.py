import pytest
import requests
from test_email import domain, user_agent, register_email, send_verify_code_email, log_er, valid_email, login
from test_phone import register_phone, send_verify_code_sms, valid_phone_num

# Test inputs
password = "password123"


def get_player_info(register_token):  # Passing in token here to prevent scope issues
    if register_token:
        response = requests.get(url=domain + '/api/v1/player/info',
                                headers={'User-Agent': user_agent, 'Authorization': register_token})
        log_er.log_info(f" Get Player Info Response Data: {response.json()}")
        # response.raise_for_status()
        return response.json()
    else:
        return "No json obtained."


def test_get_player_info_email():
    """Able to get Player Info of user who registered with email."""
    # Step 1 : Send verify code first.
    verify_code_response = send_verify_code_email(valid_email)
    if not verify_code_response:
        assert verify_code_response
    # Step 2 : Register with email (global variable in test_email.py)
    register_response = register_email(first_name="Natalie", last_name="Portman",
                                       password=password, verify_code="6666", email=valid_email)
    # Step 3 : Obtained token to be used for getting player info
    if register_response["status_code"] == 200:
        get_player_info(register_response["response"])
    else:
        log_er.log_info(f" Failed to register with email. Error: {register_response['response']}")
    assert register_response["status_code"] == 200


def test_get_player_info_phone():
    """Able to get Player Info of user who registered with phone number."""
    # Step 1 : Send verify code first.
    verify_code_response = send_verify_code_sms(valid_phone_num)
    if not verify_code_response:
        assert verify_code_response
    # Step 2 : Register with email (global variable in test_email.py)
    register_response = register_phone(first_name="Claire", last_name="Danes",
                                       password=password, verify_code="6666", phone_num=valid_phone_num)
    # Step 3 : Obtained token to be used for getting player info
    if register_response["status_code"] == 200:
        get_player_info(register_response["response"])
    else:
        log_er.log_info(f" Failed to register with phone number. Error: {register_response['response']}")
    assert register_response["status_code"] == 200


def test_update_nickname_email():
    """Able to change nickname of a player."""
    nickname_new_value = "Princess Amidala"
    # Assuming the above test case has been run prior to this.
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/nickname",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": nickname_new_value})
        if response.status_code == 200:
            log_er.log_info(f" Nickname Update Value: \'{nickname_new_value}\'")
            get_player_info(token)
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_update_club_name_email():
    """Able to change club name."""
    club_name_new_value = "Black Pink Fan Club"
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/club-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": club_name_new_value})
        if response.status_code == 200:
            log_er.log_info(f" Club Name Update Value: \'{club_name_new_value}\'")
            get_player_info(token)
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_update_icon_index_email():
    """Able to change nickname of a player"""
    head_icon_new_index = "7e53nt"
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/head-icon",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": head_icon_new_index})
        if response.status_code == 200:
            log_er.log_info(f" Head Icon Index new value: {head_icon_new_index}")
            get_player_info(token)
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_get_generated_name_email():
    """Able to change nickname of a player"""
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.get(url=domain + "/api/v1/player/system-generated-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                params={"player-name-type": "NICK_NAME"})
        if response.status_code == 200:
            log_er.log_info(f" Name successfully generated. Provided name: {response.content.decode()}")
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_update_nickname_phone():
    """Able to change nickname of a player."""
    nickname_new_value = "Ice Queen"
    # Assuming the above test case has been run prior to this.
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/nickname",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": nickname_new_value})
        if response.status_code == 200:
            log_er.log_info(f" Nickname Update Value: \'{nickname_new_value}\'")
            get_player_info(token)
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_update_club_name_phone():
    """Able to change club name."""
    club_name_new_value = "Astronomy Club"
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/club-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": club_name_new_value})
        if response.status_code == 200:
            log_er.log_info(f" Club Name Update Value: \'{club_name_new_value}\'")
            get_player_info(token)
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


@pytest.mark.skip  # There is only one known index in the server.
def test_update_icon_index_phone():
    """Able to change nickname of a player"""
    head_icon_new_index = "7e53nt"
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/head-icon",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": head_icon_new_index})
        if response.status_code == 200:
            log_er.log_info(f" Head Icon Index new value: {head_icon_new_index}")
            get_player_info(token)
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_get_generated_name_phone():
    """Able to change nickname of a player"""
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.get(url=domain + "/api/v1/player/system-generated-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                params={"player-name-type": "NICK_NAME"})
        if response.status_code == 200:
            log_er.log_info(f" Name successfully generated. Provided name: {response.content.decode()}")
            get_player_info(token)
        else:
            log_er.log_info(f" Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200
