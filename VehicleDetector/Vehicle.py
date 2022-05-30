class Vehicle:
    def __init__(self, object_id):
        self.vehicle_id = object_id
        self.frames = []

    def get_id(self):
        return self.vehicle_id

    def add_frame(self, frame):
        self.frames.append(frame)

    def print_data(self, end_sign='\n'):
        print("vehicle_id: " + self.vehicle_id, end=end_sign)
