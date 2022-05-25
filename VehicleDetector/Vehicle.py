class Vehicle:
    def __init__(self, object_id, isClosed=False):
        self.id = object_id
        self.isClosed = isClosed

    def close_object(self):
        self.isClosed = True

    def get_id(self):
        return self.id

    def print_data(self, end_sign='\n'):
        print("id: " + self.id + ", isClosed: " + str(self.isClosed), end=end_sign)
