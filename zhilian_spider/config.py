class Dev():
    mongo_server = {
        "host": "server.asppj.top",
        "port": 27017,
        "db": "zhilian",
        "user": "zhilian_db",
        "pwd": "zhilian_db123"
    }


class Config(Dev):
    pass


config = Config
