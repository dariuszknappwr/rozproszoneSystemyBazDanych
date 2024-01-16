from pymongo import MongoClient, errors

class MongoDBConnection:
    _instance = None
    DB_NAME = 'your_database_name'

    @staticmethod
    def getInstance():
        if MongoDBConnection._instance == None:
            MongoDBConnection()
        return MongoDBConnection._instance

    def __init__(self):
        if MongoDBConnection._instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoDBConnection._instance = self
            self.client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)

    def get_database(self):
        return self.client[self.DB_NAME]
    
    def get_users_collection(self):
        return self.get_database()['users']