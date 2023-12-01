class User:
    def __init__(self, username, password, tradier_token, account_number):
        self.username = username
        self.password = password
        self.tradier_token = tradier_token
        self.account_number = account_number


    def serialize(self):
        return {
            'username': self.username,
            'password': self.password,
            'tradier_token': self.tradier_token,
            'account_number': self.account_number
        }
