MAXIMAL_FRAME_DISTANCE = 10


class Rectangle:
    def __init__(self, args):
        self.x = int(args[0])
        self.y = int(args[1])
        self.w = int(args[2])
        self.h = int(args[3])
        self.area = self.w * self.h

    def to_serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "area": self.area
        }

    def get_intersection(self, rect_b):
        x = max(self.x, rect_b.x)
        y = max(self.y, rect_b.y)
        w = min(self.x + self.w, rect_b.x + rect_b.w) - x
        h = min(self.y + self.h, rect_b.y + rect_b.h) - y
        if w < 0 or h < 0:
            return Rectangle([0, 0, 0, 0])
        else:
            return Rectangle([x, y, w, h])

    def is_similar_to(self, rect_b, th=0.5):
        intersection = self.get_intersection(rect_b)
        return (intersection.area / self.area) >= th and (intersection.area / rect_b.area) >= th

    def is_track_to(self, rectangle):
        return self.y <= rectangle.y

    def get_max_intersection(self, boxes, current_frame_name):
        max_box = None
        max_rectangle = Rectangle([0, 0, 0, 0])
        for box in boxes:
            current_rectangle = self.get_intersection(box.rectangle)
            if current_rectangle.area > max_rectangle.area\
                    and self.is_track_to(current_rectangle)\
                    and int(current_frame_name[6:-4]) - int(box.frame[6:-4]) < MAXIMAL_FRAME_DISTANCE:
                max_rectangle = current_rectangle
                max_box = box
        return max_box

    def print_data(self):
        print("x: " + str(self.x) + ", y: " + str(self.y) + ", w: " + str(self.w) + ", h: " + str(self.h))
