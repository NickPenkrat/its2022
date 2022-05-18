from collections import OrderedDict


class FrameData(object):
    def __init__(self, name, box_count, boxes):
        self.name = name
        self.box_count = box_count
        self.boxes = boxes

    def __getstate__(self):
        d = OrderedDict()
        d['name'] = self.name
        d['box_count'] = self.box_count
        d['boxes'] = self.boxes
        return d

    def print_frame_data(self):
        print('name: ' + str(self.name))
        print('box count: ' + str(self.box_count))
        print('boxes: ' + str(self.boxes))
