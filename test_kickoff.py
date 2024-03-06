import requests
import json
import pyperclip

from logger import Logger
from test_email import login

domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
log_er = Logger("KickOff")
token = login(email="my_papa@yahoo.com", password="Password123")["response"]
matchId = 0
chosen_opponent = 1


def get_opponent_id(which_player=0):
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/opposite/list',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    log_er.log_info(f"Getting opponent list \nToken: {token}")
    opponent_list_json = response.json()
    log_er.log_info(f"Opponent List Return: {opponent_list_json}")
    opponent_ids = []
    for opponent in opponent_list_json:
        opponent_ids.append(opponent['playerId'])
    log_er.log_info(f"First Opponent Id: {opponent_ids[which_player]}")
    return opponent_ids[which_player]


def refresh_opponent_list():
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/opposite/refresh',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    log_er.log_info(f"Refreshing opponent list \nToken: {token}")
    json_str = json.dumps(response.json())
    pyperclip.copy(json_str)
    return response.status_code


def get_opponent_home_team_info():
    opponent = get_opponent_id(chosen_opponent)
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/opposite/home-team-info',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token},
                            params={'oppositePlayerId': opponent})
    log_er.log_info(f"Getting opponent {opponent}  home team info \nToken: {token}")
    log_er.log_info(f"Response Status Code: {response.status_code}")
    log_er.log_info(f"{response.json()}")


def start_match():
    opponent = get_opponent_id(chosen_opponent)
    response = requests.post(url=domain + '/api/v1/kick-off/tournament/start-match',
                             headers={'User-Agent': user_agent, 'Authorization': token},
                             json={"oppositePlayerId": opponent})
    log_er.log_info(f"Starting Match... \nToken: {token}")
    log_er.log_info(f"Start Match Response Status Code: {response.status_code}")
    log_er.log_info(f"Start Match Return: {response.json()}")
    global matchId
    matchId = response.json()
    return matchId


def get_phase_result():
    global matchId
    phases = ["START", "FIRST_HALF_TIME", "SECOND_HALF_TIME", "FULL_TIME"]
    # START
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/match/phase-result',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token},
                            params={'matchId': matchId, 'phase': phases[0]})
    current_score = response.json()
    log_er.log_info(f"Score at Start... User {current_score['scores']['mine']} : "
                    f"Opponent {current_score['scores']['opposite']}")
    # FIRST_HALF
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/match/phase-result',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token},
                            params={'matchId': matchId, 'phase': phases[1]})
    current_score = response.json()
    log_er.log_info(f"Score at First Half... User {current_score['scores']['mine']} : "
                    f"Opponent {current_score['scores']['opposite']}")
    # SECOND_HALF
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/match/phase-result',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token},
                            params={'matchId': matchId, 'phase': phases[2]})
    current_score = response.json()
    log_er.log_info(f"Score at Second Half... User {current_score['scores']['mine']} : "
                    f"Opponent {current_score['scores']['opposite']}")
    # FULL_TIME
    response = requests.get(url=domain + '/api/v1/kick-off/tournament/match/phase-result',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token},
                            params={'matchId': matchId, 'phase': phases[3]})
    current_score = response.json()
    log_er.log_info(f"Score at Full Time... User {current_score['scores']['mine']} : "
                    f"Opponent {current_score['scores']['opposite']}")


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
    """ 3.1 Get tournament opposite list. """
    get_opponent_id()


def test_refresh_opponent_list():
    """ 3.2 Refresh tournament opposite list. """
    assert refresh_opponent_list() == 200


def test_get_opponent_info():
    """ 3.3 Get opposite home team info. """
    get_opponent_home_team_info()


def test_start_match():
    """ 3.4 Start Match. """
    start_match()


def test_get_phase_result():
    """ 3.5 get match phase result of different phase """
    get_phase_result()


def test_get_match_result():
    """ 3.6 Get the match result. """
    get_match_result()
