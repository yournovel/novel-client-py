class InvalidToken(Exception):
    def __init__(self, message="The API token provided is invalid. (Must be between 32-64 characters and alphanumeric)"):
        self.message = message
        super().__init__(self.message)

class InvalidKeyfile(Exception):
    def __init__(self, message="The keyfile provided is invalid. (Must be a valid PEM keyfile)"):
        self.message = message
        super().__init__(self.message)

class NoKeyfile(Exception):
    def __init__(self, message="This novel instance requires keyfile authentication, but no keyfile was provided."):
        self.message = message
        super().__init__(self.message)