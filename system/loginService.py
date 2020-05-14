import mongoCollection


class LoginService:
    def __init__(self):
        self.__user_base = mongoCollection.MongoCollection("users")
        self.__user = None

    def welcome(self):
        print("Welcome, user! If you want to log in, use \"login <username>\".")
        print("If you are new, please use \"register <username>\".")
        while self.__user is None:
            tokens = []
            while len(tokens) < 2:
                s = input()
                tokens = s.split()
            if tokens[0] == "login":
                self.login(tokens[1])
            elif tokens[0] == "register":
                self.register(tokens[1])
            else:
                print("Please, cooperate!")

    def login(self, username):
        self.__user = self.__user_base.get("username", username)
        if self.__user is None:
            print("There is no user with this name, would you like to register?")
            return
        i = 0
        while i < 3:
            password = input("Password: ")
            if self.__user["password"] == password:
                print("You are now logged in!")
                return
            else:
                i += 1
        print("You have failed to log in, continuing as anonymous user.")
        self.__user = None

    def register(self, username):
        while self.__user is None:
            print("Please enter your new password")
            password1 = input("Password: ")
            print("Please confirm your password")
            password2 = input("Password: ")
            if password1 == password2:
                print("Password set correctly! Logging you into your new account")
                new_user = {
                    "username": username,
                    "password": password1,
                    "privileges": []  # Insert default privileges here
                }
                self.__user_base.send(new_user)
                self.__user = new_user
            else:
                print("You have given two different passwords, you shouldn't do that.")
                print("Would you like to try again?")
                s = None
                while s is None:
                    s = input("[Y/N]")
                    if s == "Y":
                        pass
                    elif s == "N":
                        return
                    else:
                        print("Please cooperate!")
                        s = None

    def logout(self):
        print("Logging out!")
        self.__user = None

    def check_privilege(self, privilege):
        if self.__user is None:
            return False
        if privilege in self.__user["privileges"]:
            return True
        else:
            return False

    def grant_privilege(self, username, privilege):
        """Proposed privileges:
        admin - give privileges to others
        add - adding new peripheral devices
        list - listing available services
        send - sending commands to peripherals
        dev_<devname> access to specific device
        """
        if self.__user is None:
            print("You can't grant privileges to others without logging in!")
            return False
        if "admin" in self.__user["privileges"]:
            user_to_grant = self.__user_base.get("username", username)
            if user_to_grant is None:
                print("There is no such user!")
                return False
            user_to_grant["privileges"].append(privilege)
            self.__user_base.remove("username", username)
            self.__user_base.send(user_to_grant)
            return True
        else:
            print("You have to be an admin to give privileges to others!")
            return False

    def revoke_privilege(self, username, privilege):
        if self.__user is None:
            print("You can't grant privileges to others without logging in!")
            return False
        if "admin" in self.__user["privileges"]:
            user_under_question = self.__user_base.get("username", username)
            if user_under_question is None:
                print("There is no such user!")
                return False
            if privilege in user_under_question["privileges"]:
                user_under_question["privileges"].remove(privilege)
                self.__user_base.remove("username", username)
                self.__user_base.send(user_under_question)
                return True
            else:
                print("The user doesn't have this privilege")
                return False
        else:
            print("You have to be an admin to give privileges to others!")
            return False
