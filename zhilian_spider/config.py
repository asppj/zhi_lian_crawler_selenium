class Dev():
    mongo_server = {
        "host": "你的host",
        "port": 27017,
        "db": "zhilian",
        "user": "你的",
        "pwd": "你的"
    }


class Config(Dev):
    pass


config = Config
