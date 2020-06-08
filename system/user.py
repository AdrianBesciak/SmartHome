from system import mongoCollection


class User:
    db = mongoCollection.MongoCollection('Users')

    def __init__(self, username, email, password, privileges):
        self.username = username
        self.email = email
        self.__password = password
        self.privileges=privileges
        self.is_authenticated = False
        self.is_active = False
        self.is_anonymous = True
        # self.__send_to_db__()

    def send_to_db(self):
        self.db.send({
            "username": self.username,
            "email": self.email,
            "password": self.__password,
            "privileges": self.privileges
        })

    def check_privilege(priv):
        if priv in self.privileges:
            return True
        return False

    def auth(self, bool):
        if bool:
            self.is_authenticated = True
            self.is_active = True
            self.is_anonymous = False
        else:
            self.is_authenticated = False
            self.is_active = False
            self.is_anonymous = True

    def get_password(self):
        return self.__password

    def get_id(self):
        return self.email



    def is_authenticated(self):
        return (self.username is not None) and (self.__password is not None)

    @staticmethod
    def get_by_email(email):
        user_dict = User.db.get('email', email)
        if user_dict is not None:
            user = User(user_dict['username'], user_dict['email'], user_dict['password'],user_dict['privileges'] )
            user.auth(True)
            return user
        else:
            user = User(None, None, None, [])
            user.auth(False)
            return user
