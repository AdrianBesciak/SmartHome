from system import mongoCollection
from flask_login import AnonymousUserMixin


class User(AnonymousUserMixin):
    db = mongoCollection.MongoCollection('Users')

    def __init__(self, username, email, password, privileges):
        self.username = username
        self.email = email
        self.__password = password
        self.privileges=privileges
        self.is_authenticated = False
        #self.is_active = False
        #self.is_anonymous = True
        # self.__send_to_db__()
        self.id=None

    def send_to_db(self):
        self.db.send({
            "username": self.username,
            "email": self.email,
            "password": self.__password,
            "privileges": self.privileges
        })

    def check_privilege(self, priv):
        if priv in self.privileges:
            return True
        return False

    def is_admin(self):
        return self.check_privilege('admin')

    def auth(self, bool):
        if bool:
            self.is_authenticated = True
            #self.is_active = True
            #self.is_anonymous = False
        else:
            self.is_authenticated = False
            #self.is_active = False
            #self.is_anonymous = True

    def get_password(self):
        return self.__password

    def get_id(self):
        if self.id is None:
            self_dict = User.db.get('email', self.email)
            if self_dict is not None:
                self.id = self_dict['_id']
        return str(self.id)

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
