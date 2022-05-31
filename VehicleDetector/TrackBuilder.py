from Vehicle import Vehicle
from Rectangle import Rectangle


class TrackBuilder:
    def __init__(self):
        self.track_storage = {}
        self.object_count = 0

    def add_new_object(self, framedata, index):
        object_id = str(self.object_count + 1)
        vehicle = Vehicle(object_id)
        vehicle.set_last_frame(framedata.number)
        framedata.box_objects.append(vehicle)
        self.track_storage[vehicle] = [framedata.boxes[index]]
        self.object_count += 1

    def add_to_object(self, framedata, index):
        rectangle = Rectangle(framedata.boxes[index])
        max_key = rectangle.get_max_intersection(self.track_storage, framedata.number)
        if max_key is None:
            return False
        else:
            max_key.set_last_frame(framedata.number)
            framedata.box_objects.append(max_key)
            self.track_storage[max_key].append(framedata.boxes[index])
            return True

    def build_track(self, framedata, previous_framedata=None):
        if len(self.track_storage) == 0:
            for i in range(framedata.box_count):
                self.add_new_object(framedata, i)
        else:
            for i in range(framedata.box_count):
                rectangle = Rectangle(framedata.boxes[i])
                max_index = rectangle.get_max_intersection_array(previous_framedata.boxes)
                max_key = previous_framedata.box_objects[max_index]
                if max_index == -1 \
                        or not rectangle.is_similar_to(Rectangle(previous_framedata.boxes[max_index])):
                    if not self.add_to_object(framedata, i):
                        self.add_new_object(framedata, i)
                else:
                    max_key.set_last_frame(framedata.number)
                    framedata.box_objects.append(max_key)
                    self.track_storage[max_key].append(framedata.boxes[i])

    def print_track_storage(self):
        print(self.track_storage)
