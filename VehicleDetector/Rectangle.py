class Rectangle:
    def __init__(self, args):
        self.x = args[0]
        self.y = args[1]
        self.w = args[2]
        self.h = args[3]
        self.area = self.w * self.h

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

    def get_max_intersection(self, dictionary):
        max_key = None
        max_rectangle = Rectangle([0, 0, 0, 0])
        for key in dictionary.keys():
            current_rectangle = self.get_intersection(Rectangle(dictionary[key][-1]))
            if current_rectangle.area > max_rectangle.area:
                max_rectangle = current_rectangle
                max_key = key
        return max_key
