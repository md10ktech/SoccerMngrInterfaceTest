import requests
from logger import Logger
from test_email import domain, user_agent, register_email, send_verify_code_email
import time

log_er = Logger("SoccerManager")
token = ""  # Same token to be used for all test runs in this script


def get_player_info(register_token):  # Passing in token here to prevent scope issues
    if register_token:
        response = requests.get(url=domain + '/api/v1/player/info',
                                headers={'User-Agent': user_agent, 'Authorization': register_token})
        # response.raise_for_status()
        return response.json()
    else:
        return "No json obtained."


def test_get_player_info():
    """Able to get Player Info. """
    # Step 1 : Send verify code first. If it returns "vc not expired", continue to step 2.
    verify_code_response = send_verify_code_email()
    # Step 2 : Register with email (global variable in test_email.py)
    vc_error = verify_code_response["error"]
    if verify_code_response['status_code'] == 200:
        
        register_response = register_email(first_name="Natalie", last_name="Portman",
                                           password="Thor1234", verify_code="6666")
    # Step 3 : Obtained token to be used for getting player info
        if register_response["status_code"] == 200:
            global token
            token = register_response["response"]
            log_er.log_info(f" Data: {get_player_info(token)}")
        else:
            log_er.log_info(f" Failed to register with email: {register_response['response']}")
        assert register_response["status_code"] == 200
    else:
        log_er.log_info(f" Failed to obtain verify code: {verify_code_response['error']}")
        assert verify_code_response['status_code'] == 200


def test_update_nickname():
    """Able to change nickname of a player."""
    response = requests.put(url=domain + "/api/v1/player/nickname",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            json={"updateValue": "Maverick"})
    if response.status_code == 200:
        log_er.log_info(f" Response: Nickname successfully updated.")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_update_club_name():
    """Able to change club name."""
    response = requests.put(url=domain + "/api/v1/player/club-name",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            json={"updateValue": "Arsenal F. C."})
    if response.status_code == 200:
        log_er.log_info(f" Response: Club name successfully updated.")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_update_head_icon_index():
    """Able to change nickname of a player"""
    response = requests.put(url=domain + "/api/v1/player/head-icon",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            json={"updateValue": "7e53nt"})
    if response.status_code == 200:
        log_er.log_info(f" Response: Head icon index successfully updated.")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_get_generated_name():
    """Able to change nickname of a player"""
    response = requests.get(url=domain + "/api/v1/player/system-generated-name",
                            headers={'User-Agent': user_agent, "Authorization": token},
                            params={"player-name-type": "NICK_NAME"})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200
