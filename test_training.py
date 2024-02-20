import requests
import json

from logger import Logger
from test_email import login

domain = "https://soccer-manager-qa.qq72bian.com"
user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 "
              "Safari/537.36")
log_er = Logger("SquadPlanner")

# --- LOGIN --- #
token = login(email="losangeles@gmail.com", password="Password123")["response"]
common_request = {"squadType": "null", "setIndex": 0,
                  "squadPosition": {"position": 0, "soccerPlayerId": "0"}, "playerPosition": "null"}


def get_ongoing_training():
    response = requests.get(url=domain + '/api/v1/training/record/current',
                            headers={'Content-Type': 'application/json', 'User-Agent': user_agent,
                                     'Authorization': token})
    if response.status_code == 400:
        return response.json()
    else:
        return response.status_code


def test_get_ongoing_training():
    """ 4.2 Get ongoing training status"""
    assert get_ongoing_training() == 200
