import random
import string


def get_random_domain():
    domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]
    return random.choice(domains)


def get_random_name(length):
    return ''.join(random.choice(string.ascii_lowercase[:12]) for i in range(length))


def generate_random_email():
    return get_random_name(12) + '@' + get_random_domain()
