import pytest
import requests
from logger import Logger
from datetime import datetime
from test_email import domain, user_agent

log_er = Logger("SoccerManager")


def test_get_player_info(get_token_from_email_login):
    """Able to get Player Info. """
    response = requests.get(url=domain + '/api/v1/player/info',
                            headers={'User-Agent': user_agent, 'Authorization': get_token_from_email_login})
    # response.raise_for_status()
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()} Timestamp: {datetime.now().strftime('%I:%M:%S%p')}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_update_nickname(get_token_from_email_login):
    """Able to change nickname of a player."""
    response = requests.put(url=domain + "/api/v1/player/nickname",
                            headers={'User-Agent': user_agent, "Authorization": get_token_from_email_login},
                            json={"updateValue": "Maverick"})
    if response.status_code == 200:
        log_er.log_info(f" Response: Nickname successfully updated.")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_update_club_name(get_token_from_email_login):
    """Able to change club name."""
    response = requests.put(url=domain + "/api/v1/player/club-name",
                            headers={'User-Agent': user_agent, "Authorization": get_token_from_email_login},
                            json={"updateValue": "Arsenal F. C."})
    if response.status_code == 200:
        log_er.log_info(f" Response: Club name successfully updated.")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_update_head_icon_index(get_token_from_email_login):
    """Able to change nickname of a player"""
    response = requests.put(url=domain + "/api/v1/player/head-icon",
                            headers={'User-Agent': user_agent, "Authorization": get_token_from_email_login},
                            json={"updateValue": "7e53nt"})
    if response.status_code == 200:
        log_er.log_info(f" Response: Head icon index successfully updated.")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200


def test_get_generated_name(get_token_from_email_login):
    """Able to change nickname of a player"""
    response = requests.get(url=domain + "/api/v1/player/system-generated-name",
                            headers={'User-Agent': user_agent, "Authorization": get_token_from_email_login},
                            params={"player-name-type": "NICK_NAME"})
    if response.status_code == 200:
        log_er.log_info(f" Response: {response.content.decode()}")
    else:
        log_er.log_info(f" Response: {response.json()}")
    assert response.status_code == 200

