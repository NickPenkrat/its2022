class Box:
    def __init__(self, object_id, conf, object_class, rectangle, frame):
        self.object_id = object_id
        self.conf = conf
        self.object_class = object_class
        self.rectangle = rectangle
        self.frame = frame

    def to_serialize(self):
        return {
            "frame": self.frame,
            "id": self.object_id,
            "conf": self.conf,
            "class": self.object_class,
            "rectangle": self.rectangle.to_serialize()
        }

    def change_id(self, new_id):
        self.object_id = new_id

    def print_data(self):
        print("frame: " + self.frame)
        print("id: " + str(self.object_id))
        print("confidence: " + str(self.conf))
        print("object class: " + str(self.object_class))
        self.rectangle.print_data()
