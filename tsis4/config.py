import json

# DATABASE
def load_config():
    return {
        "dbname": "snake_db",
        "user": "postgres",
        "password": "192837",
        "host": "127.0.0.1",
        "port": "5432",
        "sslmode": "disable"
    }

# SETTINGS 
def load_settings():
    try:
        with open("tsis4/settings.json", "r") as f:
            return json.load(f)
    except:
        return {
            "snake_color": [0, 255, 0],
            "grid": True,
            "sound": True
        }

def save_settings(data):
    with open("tsis4/settings.json", "w") as f:
        json.dump(data, f)