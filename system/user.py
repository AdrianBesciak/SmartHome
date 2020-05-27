from system import mongoCollection

db = mongoCollection.MongoCollection('Users')





class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.__password = password
        self.__send_to_db__()

    def __send_to_db__(self):
        self.db.send({
            "username": self.username,
            "email": self.email,
            "password": self.__password
        })

    def get_password(self):
        return self.__password
