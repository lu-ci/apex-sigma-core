import pymongo


class Database(pymongo.MongoClient):
    def __init__(self, db_cfg):
        if db_cfg.auth:
            db_address = f'mongodb://{db_cfg.username}:{db_cfg.password}@{db_cfg.host}:{db_cfg.port}/'
        else:
            db_address = db_cfg.host
        super().__init__(db_address)
