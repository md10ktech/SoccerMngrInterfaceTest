import requests
import json
import pyperclip

from logger import Logger
from test_email import login

domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")

log_er = Logger("SquadPlanner")
token = login(email="yes@yes.com", password="123456Aa")["response"]
common_request = {"squadType": "null", "setIndex": 0,
                  "squadPosition": {"position": 0, "soccerPlayerId": "0"}, "playerPosition": "null"}


def get_player_template(role_position, player_id, role):
    return {"squadPosition": {"position": role_position, "soccerPlayerId": player_id},
            "playerPosition": role}


def get_all_soccer_players_info():
    """ 6.1 Get info of all soccer players for a user (account). """
    log_er.log_info(f" -Login Token: \n{token}")
    response = requests.get(url=domain + '/api/v1/squad/soccer-player/all',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    if response.status_code == 200:
        log_er.log_info(f" -Get All Soccer Players Successful.")
        json_str = json.dumps(response.json())
        pyperclip.copy(json_str)
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
        soccer_player_ids.append((player["id"], player["playerPosition"]))
    log_er.log_info(f" {soccer_player_ids}")
    return soccer_player_ids


def remove_slot(squad_type, preset, role_position, player_id, role):
    """ 6.7 Remove Formation Soccer Slot - Actually, completely removes a slot from the squad."""
    response = requests.put(url=domain + '/api/v1/squad/formation/remove-soccer-slot',
                            headers={'User-Agent': user_agent, 'Authorization': token},
                            json={"squadType": squad_type, "setIndex": preset,
                                  "squadPosition": {"position": role_position, "soccerPlayerId": player_id},
                                  "playerPosition": role})
    if response.status_code == 400:
        log_er.log_info(response.json())
    return response.status_code


def test_remove_slot():
    """ Remove A Player Slot"""
    # 1. Able to remove with proper input
    # status = remove_slot("HOME", 0, 1, "956177718774591488", "FW")
    # 2. Able to remove with player id = 0
    # status = remove_slot("HOME", 0, 2, "0", "FW")
    # 3. Able to remove with a player id elsewhere in the squad
    # status = remove_slot("HOME", 0, 1, "956177718787174401", "MID")
    # 4. Able to remove with non-existent player id
    # status = remove_slot("HOME", 0, 1, "90123456789", "DEF")
    # 5. Able to remove with role position outside range - returns success!
    status = remove_slot("HOME", 0, 5, "0", "FW")

    get_squad_info()
    assert status == 200


def autofill_4_4_2():
    """ 6.9 auto fill formation slot. """
    position = 1
    # player_ids = []
    players = []
    all_soccer_players_json = get_all_soccer_players_info()

    # logic difficulty with dictionaries
    for player in all_soccer_players_json:
        if player["playerPosition"] == "FW" and position <= 2:
            # player_ids.append((player['id'], player['playerPosition']))
            players.append(get_player_template(position, player['id'], "FW"))
            position += 1
        elif player["playerPosition"] == "MID" and 2 < position <= 6:
            # player_ids.append((player['id'], player['playerPosition']))
            players.append(get_player_template(position-2, player['id'], "MID"))
            position += 1
        elif player["playerPosition"] == "DEF" and 6 < position <= 10:
            # player_ids.append((player['id'], player['playerPosition']))
            players.append(get_player_template(position-6, player['id'], "DEF"))
            position += 1
        elif player["playerPosition"] == "GK" and position == 11:
            # player_ids.append((player['id'], player['playerPosition']))
            players.append(get_player_template(0, player['id'], "GK"))
            position += 1
    log_er.log_info(players)


def test_get_all_soccer_players_info():
    """ Get info of all the soccer players. """
    get_all_soccer_players_info()
    assert True


def test_get_squad_info():
    """ Get Squad Information. """
    get_squad_info()
    assert True


def test_get_autofill_players():
    """ After choosing strategy, the affected squad is updated. """
    autofill_4_4_2()
    assert True
