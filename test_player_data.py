import pytest
import requests
from test_email import domain, user_agent, register_email, send_verify_code_email, log_er, login
from test_phone import register_phone, send_verify_code_sms
from random_email_mobile import randomize_email, randomize_mobile_num

# Test inputs
password = "Password123"
valid_email = randomize_email()
valid_phone_num = randomize_mobile_num()


def get_player_info(register_token):  # Passing in token here to prevent scope issues
    if register_token:
        response = requests.get(url=domain + '/api/v1/player/info',
                                headers={'User-Agent': user_agent, 'Authorization': register_token})
        log_er.log_info(f" -Get Player Info Response Data: {response.json()}")
        # response.raise_for_status()
        return response.json()
    else:
        return "No json obtained."

# -------------------- EMAIL -------------------- #


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
    assert register_response["status_code"] == 200


def test_update_nickname_email():
    """Able to change nickname of a player who registered with email."""
    nickname_new_value = "I Am Batman"
    # Assuming the above test case has been run prior to this.
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/nickname",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": nickname_new_value})
        log_er.log_info(f" -Nickname Update Value: \'{nickname_new_value}\'")
        if response.status_code == 200:
            get_player_info(token)
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_update_club_name_email():
    """Able to change club name of a player who registered with email."""
    club_name_new_value = "Gastronomy Club"
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/club-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": club_name_new_value})
        log_er.log_info(f" -Club Name Update Value: \'{club_name_new_value}\'")
        if response.status_code == 200:
            get_player_info(token)
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_update_icon_index_email():
    """Able to change icon index of a player who registered with email."""
    head_icon_new_index = "2"  # 7e53nt
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/head-icon",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": head_icon_new_index})
        log_er.log_info(f" -Head Icon Index new value: {head_icon_new_index}")
        if response.status_code == 200:
            get_player_info(token)
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200


def test_get_generated_name_email():
    """Able to generate nickname of a player who registered with email."""
    login_response = login(email=valid_email, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.get(url=domain + "/api/v1/player/system-generated-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                params={"player-name-type": "NICK_NAME"})
        if response.status_code == 200:
            log_er.log_info(f" -Name successfully generated. Provided name: {response.content.decode()}")
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info(" -Unable to retrieve token with provided email.")
        assert login_response['status_code'] == 200

# -------------------- PHONE -------------------- #


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
    assert register_response["status_code"] == 200


def test_update_nickname_phone():
    """Able to change nickname of a player who registered with phone number."""
    nickname_new_value = "Aussie Actress"
    # Assuming the above test case has been run prior to this.
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/nickname",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": nickname_new_value})
        log_er.log_info(f" -Nickname Update Value: \'{nickname_new_value}\'")
        if response.status_code == 200:
            get_player_info(token)
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info("U -Unable to retrieve token with provided phone.")
        assert login_response['status_code'] == 200


def test_update_club_name_phone():
    """Able to change club name of a player who registered with phone number."""
    club_name_new_value = "Followers of No Name"
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.put(url=domain + "/api/v1/player/club-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": club_name_new_value})
        log_er.log_info(f" -Club Name Update Value: \'{club_name_new_value}\'")
        if response.status_code == 200:
            get_player_info(token)
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info(" -Unable to retrieve token with provided phone number.")
        assert login_response['status_code'] == 200


# @pytest.mark.skip
def test_update_icon_index_phone():
    """Able to change icon index of a player who registered with phone number."""
    head_icon_new_index = "3"  # 7e53nt
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        log_er.log_info(f" -Head Icon Index new value: {head_icon_new_index}")
        response = requests.put(url=domain + "/api/v1/player/head-icon",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                json={"updateValue": head_icon_new_index})
        if response.status_code == 200:
            get_player_info(token)
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info(" -Unable to retrieve token with provided phone number.")
        assert login_response['status_code'] == 200


def test_get_generated_name_phone():
    """Able to generate nickname of a player who registered with phone number."""
    login_response = login(phone=valid_phone_num, password=password)
    if login_response['status_code'] == 200:
        token = login_response["response"]
        response = requests.get(url=domain + "/api/v1/player/system-generated-name",
                                headers={'User-Agent': user_agent, "Authorization": token},
                                params={"player-name-type": "NICK_NAME"})
        if response.status_code == 200:
            log_er.log_info(f" -Name successfully generated. Provided name: {response.content.decode()}")
            # get_player_info(token)
        else:
            log_er.log_info(f" -Error: {response.json()}")
        assert response.status_code == 200
    else:
        log_er.log_info(" -Unable to retrieve token with provided phone number.")
        assert login_response['status_code'] == 200
