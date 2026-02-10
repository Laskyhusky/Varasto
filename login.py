import json
import bcrypt

class Loginscreen():
    def __init__(self):
        self.userfile = self.openfile("./data/users.json")
    ## Function to open a json file
    def openfile(self, filename):
        ## Opening the json file as read-only
        with open(filename, 'r') as json_file:
            ## Save the json file as a dictionary
            file = json.load(json_file)
            json_file.close()
            ## Returns the dictionary
            return file
    ## Function to match username and password
    def login(self):
        ## Input from user about username
        user_input = input("Username: ")
        ## Input from user about password
        password_input = input("Password: ")
        ## Checks every username and password combination in the json file
        for existing_user in self.userfile:
            user = self.userfile[existing_user]
            ## Matches the username in the json file with the userinput
            if user["name"] == user_input:
                ## Checks the hashed password in the json file
                stored_hash = user["password"].encode("utf-8")
                ## Checks the hashed password with the hashed password in the json file
                if bcrypt.checkpw(
                    password_input.encode("utf-8"),
                    stored_hash
                ):
                    print("Login successful!")
                    return
        print("Invalid username or password")


if __name__ == '__main__':
    mylogin = Loginscreen()
    mylogin.login()