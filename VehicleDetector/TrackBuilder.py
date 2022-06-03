class TrackBuilder:
    def __init__(self):
        # {id: [all the boxes with this id]}
        self.track_storage = {}
        self.object_count = 0

    def to_serialize(self):
        d = {}
        for key in self.track_storage.keys():
            d[key] = [box.to_serialize() for box in self.track_storage[key]]
        return d

    def add_new_object(self, box):
        self.track_storage[box.object_id] = [box]
        self.object_count += 1

    def add_to_object(self, box):
        rectangle = box.rectangle
        last_boxes = [self.track_storage[key][-1] for key in self.track_storage.keys()]
        max_box = rectangle.get_max_intersection(last_boxes, box.frame)
        if max_box is None:
            return False
        else:
            box.change_id(max_box.object_id)
            self.track_storage[max_box.object_id].append(box)
            return True

    def build_track(self, framedata, previous_framedata=None):
        if len(self.track_storage) == 0:
            for box in framedata.boxes:
                self.add_new_object(box)
        else:
            for box in framedata.boxes:
                rectangle = box.rectangle
                max_box = rectangle.get_max_intersection(previous_framedata.boxes, box.frame)
                if max_box is None \
                        or not rectangle.is_similar_to(max_box.rectangle):
                    if not self.add_to_object(box):
                        self.add_new_object(box)
                else:
                    box.change_id(max_box.object_id)
                    self.track_storage[max_box.object_id].append(box)
        return framedata
