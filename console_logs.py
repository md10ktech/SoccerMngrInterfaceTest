logs = []


def clean_log(dirty_log) -> str:
    message_list = dirty_log.split()
    message_list.pop(1)
    message_list.pop(0)
    message = " ".join(message_list)
    return message


def get_browser_logs(driver):
    console_logs = []
    for log in driver.get_log('browser'):
        if log['level'] == 'INFO' or log['level'] == 'ERRORS':
            console_log = clean_log(log['message'])
            console_logs.append(console_log)

    # print(console_logs)
    if not console_logs:
        pass
    else:
        global logs
        logs = logs + console_logs
    return console_logs


def get_all_logs():
    return logs
