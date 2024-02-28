import requests
import json
import pyperclip

from logger import Logger
from test_email import login

domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
log_er = Logger("KickOff")
token = login(email="emmastone@gmail.com", password="Password123")["response"]
matchId = 0


def get_opponent_list():
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/opposite/list',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    log_er.log_info(f"Getting opponent list \nToken: {token}")
    opponent_list_json = response.json()
    log_er.log_info(f"{opponent_list_json}")
    opponent_ids = []
    for opponent in opponent_list_json:
        opponent_ids.append(opponent['playerId'])
    log_er.log_info(f"First Opponent Id: {opponent_ids[0]}")
    return opponent_ids[0]


def refresh_opponent_list():
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/opposite/refresh',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    log_er.log_info(f"Refreshing opponent list \nToken: {token}")
    json_str = json.dumps(response.json())
    pyperclip.copy(json_str)
    return response.status_code


def get_opponent_home_team_info():
    first_opponent = get_opponent_list()
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/opposite/home-team-info',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token},
                            params={'oppositePlayerId': first_opponent})
    log_er.log_info(f"Getting opponent {first_opponent}  home team info \nToken: {token}")
    log_er.log_info(f"Response Status Code: {response.status_code}")
    log_er.log_info(f"{response.json()}")


def start_match():
    first_opponent = get_opponent_list()
    response = requests.post(url=domain + '/api/v1/kick-off/tournament/start-match',
                             headers={'User-Agent': user_agent, 'Authorization': token},
                             json={"oppositePlayerId": first_opponent})
    log_er.log_info(f"Starting Match... \nToken: {token}")
    log_er.log_info(f"Response Status Code: {response.status_code}")
    log_er.log_info(f"{response.json()}")
    global matchId
    matchId = response.json()
    return matchId


def get_match_result():
    global matchId
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/match/result',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token},
                            params={'matchId': matchId}
                            )
    log_er.log_info(f"Getting match results \nToken: {token}")
    log_er.log_info(f"Response Status Code: {response.status_code}")
    log_er.log_info(f"{response.json()}")

# ---------- TEST FUNCTIONS ---------- #


def test_get_opponent_list():
    """ 5.1 Get tournament opposite list. """
    get_opponent_list()


def test_refresh_opponent_list():
    """ 5.2 Refresh tournament opposite list. """
    assert refresh_opponent_list() == 200


def test_get_opponent_info():
    """ 5.3 Get opposite home team info. """
    get_opponent_home_team_info()


def test_start_match():
    """ 5.4 Start Match. """
    start_match()


def test_get_match_result():
    """ 5.6 Get the match result. """
    get_match_result()
