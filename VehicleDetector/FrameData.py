from collections import OrderedDict


class FrameData(object):
    def __init__(self, name, box_count, boxes):
        self.name = name
        self.box_count = box_count
        self.boxes = boxes
        self.box_objects = []

    def __getstate__(self):
        d = OrderedDict()
        d['name'] = self.name
        d['box_count'] = self.box_count
        d['boxes'] = self.boxes
        d['box_objects'] = self.box_objects
        return d

    def set_box_objects(self, box_objects):
        self.box_objects = box_objects

    def print_frame_data(self):
        print('name: ' + str(self.name))
        print('box count: ' + str(self.box_count))
        print('boxes: ' + str(self.boxes))
        print('box_objects:')
        for box in self.box_objects:
            box.print_data()
