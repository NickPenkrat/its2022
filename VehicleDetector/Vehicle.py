class Vehicle:
    def __init__(self, object_id):
        self.id = object_id
        self.isClosed = False

    def close_object(self):
        self.isClosed = True

    def get_id(self):
        return self.id
