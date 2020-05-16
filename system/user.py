from system import mongoCollection


class User:
    def __init__(self, username, email, password):
        self.db = MongoCollection('Users')
        self.username = username
        self.email = email
        self.__password = password

    def __send_to_db__(self):
        self.db.send({
            "username": self.username,
            "email": self.email,
            "password": self.__password
        })

    def get_password(self):
        return self.__password
