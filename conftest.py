import pytest
# import requests
import email_report


def pytest_sessionfinish(session, exitstatus):
    email_report.send_email_report(f"Soccer Manager API Test Results")


# This is currently setup to change the values of the node id to documentation strings added in test functions.
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    test_fn = item.obj
    docstring = getattr(test_fn, '__doc__')
    if docstring:
        # This is where you can change values of attributes with docstring
        report.nodeid = docstring


# @pytest.fixture
# def get_token_from_email_login():
#     response = requests.post(url=domain + '/api/v1/player/login/email/login',
#                              headers={'User-Agent': user_agent},
#                              json={"pwd": "password123",
#                                    "email": user_email})
#     if response.status_code == 200:
#         return response.content.decode()
#     else:
#         return response.json()


# @pytest.fixture
# def get_token_from_phone_login():
#     response = requests.post(url=domain + '/api/v1/player/login/sms/login',
#                              headers={'User-Agent': user_agent},
#                              json={"pwd": "password123",
#                                    "telNo": "1234567890"})
#     if response.status_code == 200:
#         return response.content.decode()
#     else:
#         return response.json()
