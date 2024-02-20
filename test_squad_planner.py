import requests
import json
import pyperclip

from logger import Logger
from test_email import login

domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
log_er = Logger("SquadPlanner")

# --- LOGIN --- #
token = login(email="emmastone@gmail.com", password="Password123")["response"]
common_request = {"squadType": "null", "setIndex": 0,
                  "squadPosition": {"position": 0, "soccerPlayerId": "0"}, "playerPosition": "null"}


def get_player_template(role_position, player_id, role):
    return {"squadPosition": {"position": role_position, "soccerPlayerId": player_id},
            "playerPosition": role}


def recruit_soccer_players_from_gacha(recruit_num=1):
    log_er.log_info(f"Recruiting {recruit_num} new players.")
    response = requests.post(url=domain + '/api/v1/gacha/pull',
                             headers={'User-Agent': user_agent, 'Authorization': token},
                             json={"setName": "Default_Banner", "recruitNumber": recruit_num})
    return response.json()


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


def get_all_players_role_id():
    """ 6.1 Get IDs of each soccer player that exists in an account. """
    soccer_player_ids = []
    all_soccer_players_json = get_all_soccer_players_info()
    for player in all_soccer_players_json:
        soccer_player_ids.append({"role": player["playerPosition"], "id": player["id"]})
    log_er.log_info(f" {soccer_player_ids}")
    # pyperclip.copy(soccer_player_ids)
    # log_er.log_info(f" All soccer players copied to clipboard.")
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

    fill_count = 0  # position must start from 0 - left to right
    players = []
    autofill_request_json = {"squadType": squad_type, "setIndex": preset, "items": []}
    all_soccer_players_json = get_all_soccer_players_info()

    mid_count = formation[0] + formation[1]

    for player in all_soccer_players_json:
        if player["playerPosition"] == "DEF" and fill_count < formation[0]:
            players.append(get_player_template(fill_count, player['id'], "DEF"))
            fill_count += 1

    for player in all_soccer_players_json:
        if player["playerPosition"] == "MID" and formation[0] <= fill_count < mid_count:
            players.append(get_player_template(fill_count - formation[0], player['id'], "MID"))
            fill_count += 1

    for player in all_soccer_players_json:
        if player["playerPosition"] == "FW" and mid_count <= fill_count < 10:
            players.append(get_player_template(fill_count - mid_count, player['id'], "FW"))
            fill_count += 1

    for player in all_soccer_players_json:
        if player["playerPosition"] == "GK":
            players.append(get_player_template(0, player['id'], "GK"))
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


def test_get_all_players_role_id():
    """ Get info of all the soccer players. """
    get_all_players_role_id()
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
    set_formation(squad_type="HOME", preset=0, formation="FIVE_THREE_TWO")
    assert autofill_squad(squad_type="HOME", preset=0, formation=[5, 3, 2]) == 200
    get_squad_info()


def test_gacha_players_added():
    """A pull of new recruits from gacha adds to user's inventory correctly."""
    # Enter number of soccer players to recruit here.
    recruit_num = 10
    new_recruits = recruit_soccer_players_from_gacha(recruit_num)
    all_players = get_all_soccer_players_info()
    match_count = 0
    for recruit in new_recruits:
        for player in all_players:
            if player['id'] == recruit['id']:
                match_count += 1
                log_er.log_info(f"{match_count} - New recruit {player['id']} exists in user's account.")
                break
    log_er.log_info(f"Total number of players now: {len(all_players)}")
    assert match_count == recruit_num


def test_gacha_rarity_chance(recruit_num=10, times=10):
    """Check rarity percentage."""
    ssr_count = 0
    sr_count = 0
    r_count = 0
    all_new_recruits = []
    for gacha_try in range(times):
        new_recruits = recruit_soccer_players_from_gacha(recruit_num)
        for recruit in new_recruits:
            if recruit['rarity'] == "SSR":
                ssr_count += 1
            elif recruit['rarity'] == "SR":
                sr_count += 1
            elif recruit['rarity'] == "R":
                r_count += 1
            else:
                log_er.log_info("Player has no Rarity.")
        all_new_recruits.extend(new_recruits)
        # new_recruits.clear()
    total_new_recruits = len(all_new_recruits)
    ssr_percent = ssr_count / total_new_recruits
    sr_percent = sr_count / total_new_recruits
    r_percent = r_count / total_new_recruits
    log_er.log_info(f"SSR_percentage = {ssr_count} / {total_new_recruits} = {ssr_percent}")
    log_er.log_info(f"SR_percentage = {sr_count} / {total_new_recruits} = {sr_percent}")
    log_er.log_info(f"R_percentage = {r_count} / {total_new_recruits} = {r_percent}")
    pyperclip.copy(f"{ssr_percent},{sr_percent},{r_percent}")
    log_er.log_info("Copied csv.")
    assert total_new_recruits == recruit_num * times

