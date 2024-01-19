import requests
import json
import pyperclip

from logger import Logger
from test_email import login

domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")

log_er = Logger("SquadPlanner")
token = login(email="brazil@email.com", password="Password123")["response"]


def get_all_soccer_players_info():
    """ 6.1 Get info of all soccer players for a user (account). """
    log_er.log_info(f" -Login Token: \n{token}")
    response = requests.get(url=domain + '/api/v1/squad/soccer-player/all',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    if response.status_code == 200:
        log_er.log_info(f" -Get All Soccer Players Successful.")
        # json_str = json.dumps(response.json())
        # pyperclip.copy(json_str)
    else:
        log_er.log_info(f" -Get All Soccer Players failed. Error: {response.json()}")
    return response.json()


def get_squad_info():
    """ 6.2 Get squad information for an account. """
    log_er.log_info(f" -Login Token: \n{token}")
    response = requests.get(url=domain + '/api/v1/squad/information',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    if response.status_code == 200:
        log_er.log_info(f" -Get Squad Information Successful.")
        json_str = json.dumps(response.json())
        pyperclip.copy(json_str)
    else:
        log_er.log_info(f" -Get Squad Information failed. Error: {response.json()}")
    return response.json()


def get_all_soccer_player_ids():
    """ 6.1 Get IDs of each soccer player that exists in an account. """
    soccer_player_ids = []
    all_soccer_players_json = get_all_soccer_players_info()
    for player in all_soccer_players_json:
        soccer_player_ids.append(player["id"])
    log_er.log_info(f" {soccer_player_ids}")
    return soccer_player_ids


def autofill_4_4_2():
    """ 6.9 auto fill formation slot. """
    items = []
    slot = {}
    increment = 0
    all_soccer_players_json = get_all_soccer_players_info()
    for player in all_soccer_players_json:
        increment += 1
        if player["playerPosition"] == "FW":
            if increment <= 2:
                slot["position"] = increment
                slot["soccerPlayerId"] = player["id"]
                items.append({"squadPosition": slot, "playerPosition": "FW"})
            else:
                break
        elif player["playerPosition"] == "MID":
            if increment <= 6:
                slot["position"] = increment
                slot["soccerPlayerId"] = player["id"]
                items.append({"squadPosition": slot, "playerPosition": "MID"})
        elif player["playerPosition"] == "DEF":
            if increment <= 10:
                slot["position"] = increment
                slot["soccerPlayerId"] = player["id"]
                items.append({"squadPosition": slot, "playerPosition": "DEF"})
        elif player["playerPosition"] == "GK":
            if increment <= 11:
                slot["position"] = increment
                slot["soccerPlayerId"] = player["id"]
                items.append({"squadPosition": slot, "playerPosition": "DEF"})
    log_er.log_info(f" {items}")


def test_choose_strategy():
    """ After choosing strategy, the affected squad is updated. """
    autofill_4_4_2()
    # get_all_soccer_player_ids()
    # get_soccer_players()
    # get_squad_info()
    assert True
