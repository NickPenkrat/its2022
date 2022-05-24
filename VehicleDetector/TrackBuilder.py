from Rectangle import Rectangle


class TrackBuilder:
    def __init__(self):
        self.track_storage = {}
        self.object_count = 0

    def add_new_object(self, framedata, index):
        object_id = str(self.object_count + 1)
        framedata.box_objects.append(object_id)
        self.track_storage[object_id] = [framedata.boxes[index]]
        self.object_count += 1

    def add_to_object(self, framedata, index):
        rectangle = Rectangle(framedata.boxes[index])
        max_key = rectangle.get_max_intersection(self.track_storage)
        if max_key is None:
            return False
        else:
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
                count = 0
                for j in range(previous_framedata.box_count):
                    if rectangle.is_similar_to(Rectangle(previous_framedata.boxes[j])):
                        framedata.box_objects.append(previous_framedata.box_objects[j])
                        self.track_storage[previous_framedata.box_objects[j]].append(framedata.boxes[i])
                    else:
                        count += 1
                if count == previous_framedata.box_count:
                    if not self.add_to_object(framedata, i):
                        self.add_new_object(framedata, i)

    def print_track_storage(self):
        print(self.track_storage)
