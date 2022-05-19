from Rectangle import Rectangle


class TrackBuilder:
    def __init__(self):
        self.track_storage = {}
        self.object_count = 0

    def add_new_object(self, framedata, index):
        object_id = "object_" + str(self.object_count + 1)
        framedata.box_objects.append(object_id)
        self.track_storage[object_id] = [framedata.boxes[index]]
        self.object_count += 1

    def add_to_object(self, framedata, index):
        for obj in self.track_storage.keys():
            last_rect = self.track_storage[obj][-1]
            if Rectangle(framedata.boxes[index]).is_similar_to(Rectangle(last_rect), th=0.1):
                framedata.box_objects.append(obj)
                self.track_storage[obj].append(framedata.boxes[index])
                return True
        return False

    def build_track(self, framedata, previous_framedata=None):
        if len(self.track_storage) == 0:
            for i in range(framedata.box_count):
                self.add_new_object(framedata, i)
        else:
            for i in range(framedata.box_count):
                count = 0
                for j in range(previous_framedata.box_count):
                    if Rectangle(framedata.boxes[i]).is_similar_to(Rectangle(previous_framedata.boxes[j])):
                        framedata.box_objects.append(previous_framedata.box_objects[j])
                        self.track_storage[previous_framedata.box_objects[j]].append(framedata.boxes[i])
                    else:
                        count += 1
                if count == previous_framedata.box_count:
                    if not self.add_to_object(framedata, i):
                        self.add_new_object(framedata, i)

    def print_track_storage(self):
        print(self.track_storage)
