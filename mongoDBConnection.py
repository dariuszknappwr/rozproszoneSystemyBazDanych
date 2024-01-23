from pymongo import MongoClient, errors

class MongoDBConnection:
    _instance = None
    DB_NAME = 'flota_pojazdow'

    @staticmethod
    def getInstance():
        if MongoDBConnection._instance == None:
            MongoDBConnection._instance =  MongoDBConnection()
        return MongoDBConnection._instance

    def __init__(self):
        if MongoDBConnection._instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoDBConnection._instance = self
            self.client = MongoClient('mongodb://localhost:27017?directConnection=true', serverSelectionTimeoutMS=1000)
            if self.client.is_primary:
                return
            self.client = MongoClient('mongodb://localhost:27018?directConnection=true', serverSelectionTimeoutMS=1000)
            if self.client.is_primary:
                return
            self.client = MongoClient('mongodb://localhost:27019?directConnection=true', serverSelectionTimeoutMS=1000)
            if self.client.is_primary:
                return
            try:
                MongoDBConnection.getInstance().client.server_info()
            except errors.ServerSelectionTimeoutError as err:
                try:
                    self.client = MongoClient('mongodb://localhost:27018?directConnection=true', serverSelectionTimeoutMS=1000)
                    if self.client.is_primary:
                        return
                    self.client = MongoClient('mongodb://localhost:27019?directConnection=true', serverSelectionTimeoutMS=1000)
                    if self.client.is_primary:
                        return
                except errors.ServerSelectionTimeoutError as err:
                    try:
                        self.client = MongoClient('mongodb://localhost:27019?directConnection=true', serverSelectionTimeoutMS=1000)
                        if self.client.is_primary:
                            return
                    except errors.ServerSelectionTimeoutError as err:
                        print("Nie można połączyć z żadnym z serwerów")
                return

    def get_database(self):
        return self.client[self.DB_NAME]
    
    def get_users_collection(self):
        db = self.get_database()
        return db['users']
    
    def get_vehicles_collection(self):
        return self.get_database()['vehicles']
    
    def get_drivers_collection(self):
        return self.get_database()['drivers']
    
    def get_routes_collection(self):
        return self.get_database()['routes']
    
    def get_drivers_vehicles_collection(self):
        return self.get_database()['drivers_vehicles']