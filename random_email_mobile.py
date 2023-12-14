import string
import random

digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
character_list = list(string.ascii_letters) + [str(n) for n in digits]


def randomize_email(length=5):
    username = ""
    for i in range(length):
        username += random.choice(character_list)
    return username + "@email.com"


def randomize_mobile_num(length=10):
    num_str_list = [str(n) for n in digits]
    phone_num = ""
    for i in range(length):
        phone_num += random.choice(num_str_list)
    return phone_num
