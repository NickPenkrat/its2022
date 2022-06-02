class FrameData(object):
    def __init__(self, number, name, box_count, boxes):
        self.number = number
        self.name = name
        self.box_count = box_count
        self.boxes = boxes

    def to_serialize(self):
        return {
            "number": self.number,
            "name": self.name,
            "box_count": self.box_count,
            "boxes": [box.to_serialize() for box in self.boxes]
        }

    def print_frame_data(self):
        print('number: ' + str(self.number))
        print('name: ' + str(self.name))
        print('box count: ' + str(self.box_count))
        for box in self.boxes:
            box.print_data()
