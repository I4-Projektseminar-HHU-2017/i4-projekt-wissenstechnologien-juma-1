def is_empty(string: str):
    return string == "" or string is None


def is_valid_url(url):
    if isinstance(url, str):
        if not is_empty(url):
            return True
        else:
            return False
    else:
        return False
