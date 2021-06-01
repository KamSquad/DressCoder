import re


def check_uid(uid: str) -> bool:
    """
    Check uid validation
    :param uid: target uid to check
    :return:
    """
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(uid)
    return bool(match)
