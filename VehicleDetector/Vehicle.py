class Vehicle:
    def __init__(self, object_id):
        self.vehicle_id = object_id
        self.last_frame = None

    def get_last_frame(self):
        return self.last_frame

    def get_id(self):
        return self.vehicle_id

    def set_last_frame(self, frame):
        self.last_frame = frame

    def print_data(self, end_sign='\n'):
        print("vehicle_id: " + self.vehicle_id, end=end_sign)
