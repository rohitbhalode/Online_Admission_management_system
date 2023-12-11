
class Custom_Exception(Exception):
    def __init__(self):
        self.message = "The custom exception occured"
        super().__init__(self.message)