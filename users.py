class User:

    def _init(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

    def getFirstName(self):
        return self.firstName

    def getlastName(self):
        return self.lastName

    def getEmail(self):
        return self.email