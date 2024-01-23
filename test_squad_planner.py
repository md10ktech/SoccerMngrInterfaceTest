import requests
import json
import pyperclip

from logger import Logger
from test_email import login

domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")

log_er = Logger("SquadPlanner")
token = login(email="yes@no.com", password="Qwerty12")["response"]
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


def set_formation(squad_type="HOME", preset=0, formation="FOUR_FOUR_TWO"):
    """ 6.2 Set Formation for a squad. """
    response = requests.put(url=domain + '/api/v1/squad/formation',
                            headers={'User-Agent': user_agent, 'Authorization': token},
                            json={"squadType": squad_type, "setIndex": preset, "formationType": formation})
    if response.status_code == 400:
        log_er.log_info(f" -Setting formation for squad {squad_type} {preset} failed. Error: {response.json()}")
    return response.status_code


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


def autofill_squad(squad_type="HOME", preset=0, formation=None):
    """ 6.9 auto fill formation slot. """
    if formation is None:
        formation = []

    if sum(formation) > 10:
        log_er.log_info("Formation is not correct.")
        return 0
    elif len(formation) == 0:
        log_er.log_info("Formation is empty.")
        return 0

    fill_count = 1
    players = []
    autofill_request_json = {"squadType": squad_type, "setIndex": preset, "items": []}
    all_soccer_players_json = get_all_soccer_players_info()

    mid_count = formation[0] + formation[1]

    for player in all_soccer_players_json:
        if player["playerPosition"] == "FW" and fill_count <= formation[0]:
            players.append(get_player_template(fill_count, player['id'], "FW"))
            fill_count += 1

    for player in all_soccer_players_json:
        if player["playerPosition"] == "MID" and formation[0] < fill_count <= mid_count:
            players.append(get_player_template(fill_count - formation[0], player['id'], "MID"))
            fill_count += 1

    for player in all_soccer_players_json:
        if player["playerPosition"] == "DEF" and mid_count < fill_count <= 10:
            players.append(get_player_template(fill_count - mid_count, player['id'], "DEF"))
            fill_count += 1

    for player in all_soccer_players_json:
        if player["playerPosition"] == "GK":
            players.append(get_player_template(1, player['id'], "GK"))
            break

    autofill_request_json["items"] = players
    log_er.log_info(autofill_request_json)
    response = requests.put(url=domain + '/api/v1/squad/formation/auto-fill-slot',
                            headers={'User-Agent': user_agent, 'Authorization': token},
                            json=autofill_request_json)
    if response.status_code == 400:
        log_er.log_info(response.json())
    return response.status_code


def test_get_all_soccer_players_info():
    """ Get info of all the soccer players. """
    get_all_soccer_players_info()
    assert True


def test_get_squad_info():
    """ Get Squad Information. """
    get_squad_info()
    assert True


def test_remove_slot():
    """ 6.7 Remove A Player Slot"""
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


def test_get_autofill_players():
    """ 6.9 Auto-fill a squad. """
    # "FIVE_THREE_TWO" "TWO_THREE_FIVE" "THREE_FIVE_TWO"
    set_formation(squad_type="AWAY", preset=2, formation="FIVE_FOUR_ONE")
    assert autofill_squad(squad_type="AWAY", preset=2, formation=[5, 4, 1]) == 200
    get_squad_info()
