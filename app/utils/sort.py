

def get_key(key):
    try:
        return int(key)
    except ValueError:
        return key
