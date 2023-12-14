"""
Parses the json file generated as a report after a test run.
Then passed in the relevant data into the relevant tags.
This is then written onto the html file.
"""
import json
import time
import platform
from bs4 import BeautifulSoup
import console_logs as cs_logs
import math


def calc_duration(seconds):
    if seconds > 60:
        minutes = math.floor(seconds/60)
        duration_string = f"{minutes} minutes and {round(seconds - minutes*60, 2)} seconds"
    else:
        duration_string = f"{round(seconds, 2)} seconds."
    return duration_string


def parse_json_to_html(subject):
    with open(".report.json") as json_file:
        test_data = json.load(json_file)
    with open("report_body.html") as html_body_file:
        html_body = BeautifulSoup(html_body_file, 'html.parser')
    created_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(test_data["created"]))
    created_time_tag = html_body.find(name='p', id='created_time')
    created_time_tag.string = f"This report was generated on {created_time}"
    html_body.find(name='h1', id="api_test").string = f"{subject}"
    html_body.find(name='p', id='platform').string = f"Platform: {platform.platform()}"
    # print(f"Platform: {platform.platform()}")
    html_body.find(name='b', id='total_tests').string = f"{test_data['summary']['total']}"
    html_body.find(name='b', id='total_duration').string = calc_duration(test_data['duration'])
    # print(f"Test took {round(test_data['duration'], 2)} seconds to complete.")
    # "{:.2f}".format(seconds)
    if 'failed' in test_data['summary']:
        html_body.find(name='span', id='failed').string = f"Failed: {test_data['summary']['failed']}"
    if 'passed' in test_data['summary']:
        html_body.find(name='span', id='passed').string = f"Passed: {test_data['summary']['passed']}"
    if 'error' in test_data['summary']:
        html_body.find(name='span', id='errors').string = f"Errors: {test_data['summary']['error']}"
    if 'skipped' in test_data['summary']:
        html_body.find(name='span', id='skipped').string = f"Skipped: {test_data['summary']['skipped']}"
    if 'xfailed' in test_data['summary']:
        html_body.find(name='span', id='xfailed').string = f"Expected Failures: {test_data['summary']['xfailed']}"
    if 'xpassed' in test_data['summary']:
        html_body.find(name='span', id='xpassed').string = f"Unexpected Passes: {test_data['summary']['xpassed']}"
    results_table = html_body.find(name="table", id="results_table")
    log_msg = []
    for test in test_data['tests']:
        # print(f"Test: {test['keywords'][0]} | f Duration: {round(test['call']['duration'], 2)} |")

        if test['outcome'] == "error":
            log_msg.append(test['setup']['longrepr'])
        elif 'call' in test:
            if 'log' in test['call']:
                for i in range(len(test['call']['log'])):
                    log_msg.append(test['call']['log'][i]['msg'])
            # elif 'longrepr' in test['call']:
            #     log_msg.append(test['call']['longrepr'])

        details_tr = html_body.new_tag('tr')

        test_case_td = html_body.new_tag('td', attrs={'class': 'testname'})
        test_case_td.string = f"{test['nodeid']}"

        test_name_td = html_body.new_tag('td', attrs={'class': 'testname'})
        test_name_td.string = f"{test['keywords'][0]}"

        outcome_td = html_body.new_tag('td')
        outcome_span = html_body.new_tag('span', attrs={'class': f'{test["outcome"]}'})
        if test["outcome"] == "xfailed":
            outcome_span.string = "Failed Expectedly"
        elif test["outcome"] == "xpassed":
            outcome_span.string = "Passed Unexpectedly"
        else:
            outcome_span.string = f'{test["outcome"].title()}'
        outcome_td.append(outcome_span)

        duration_td = html_body.new_tag('td')

        if "call" in test:
            total_duration = round(test["setup"]["duration"] + test["call"]["duration"], 2)
            duration_td.string = f'{total_duration} seconds'
        else:
            duration_td.string = f'{round(test["setup"]["duration"], 2)} seconds'

        details_tr.append(test_case_td)
        details_tr.append(test_name_td)
        details_tr.append(outcome_td)
        details_tr.append(duration_td)

        logs_tr = html_body.new_tag('tr')
        logs_td = html_body.new_tag('td', attrs={'colspan': '4', 'class': 'logs'})

        for i in log_msg:
            logs_span = html_body.new_tag('span')
            logs_span.string = i
            logs_td.append(logs_span)
            logs_br = html_body.new_tag('br')
            logs_span.append(logs_br)
        log_msg = []

        logs_tr.append(logs_td)

        results_table.append(details_tr)
        results_table.append(logs_tr)

    info_log_table = html_body.find(name="table", id="browser_info_logs")

    for log in cs_logs.get_all_logs():
        info_log_tr = html_body.new_tag('tr')
        info_log_td = html_body.new_tag('td', attrs={'class': 'infologs'})
        log_str = str(log).strip('\"')
        info_log_td.string = log_str
        info_log_tr.append(info_log_td)
        info_log_table.append(info_log_tr)

    with open("report.html", mode="w") as report_file:
        report_file.write(str(html_body))

