import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import json_parser as json_parser

MY_EMAIL = "muhsen.10ktech@gmail.com"
GMAIL_APP_PWD = "kxwlcunxqitnoaap"

report_email = MIMEMultipart("alternative")
report_email["From"] = MY_EMAIL
report_email["To"] = MY_EMAIL


def send_email_report(subject):
    time.sleep(2)  # give some time to fully generate json file.
    json_parser.parse_json_to_html(subject)
    time.sleep(2)  # give some time to parse json data into html.

    report_filepath = f"./report.html"

    with open(report_filepath, encoding='utf-8') as report_template:
        str_list = report_template.readlines()

    content = "".join(str_list)
    report_email["Subject"] = subject
    report_email.attach(MIMEText(content, "html"))

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()  # Secures the connection
        connection.login(user=MY_EMAIL, password=GMAIL_APP_PWD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=report_email.as_string())

