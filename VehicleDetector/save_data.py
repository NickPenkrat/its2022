import cv2
import yaml
from yaml_parser import OUTPUT_FILE
from FrameData import FrameData
from Box import Box
from Rectangle import Rectangle


def deserialize_framedata(outfile):
    framedata_storage = []
    with open(outfile) as f:
        data = yaml.safe_load(f)
    for frame in data:
        boxes = []
        for item in frame["boxes"]:
            box = Box(item["object_id"],
                      item["conf"],
                      item["object_class"],
                      Rectangle([item["rectangle"]["x"],
                                 item["rectangle"]["y"],
                                 item["rectangle"]["w"],
                                 item["rectangle"]["h"]]),
                      item["frame"])
            boxes.append(box)
        framedata = FrameData(frame["number"], frame["name"], frame["box_count"], boxes)
        framedata_storage.append(framedata)
    return framedata_storage


def write_box(image, box):
    rect = box.rectangle
    cv2.rectangle(image, (rect.x, rect.y), (rect.x + rect.w, rect.y + rect.h), (25, 0, 180), 1)
    org = (rect.x, rect.y - 5)
    cv2.putText(image, str(box.object_id), org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (25, 0, 180), 1)


def save_framedata(images_folder, framedata_storage, output_folder):
    for framedata in framedata_storage:
        frame_name = framedata.name
        print("Currently saving: " + frame_name)
        img = cv2.imread(images_folder + "\\" + frame_name)
        for box in framedata.boxes:
            write_box(img, box)
        cv2.imwrite(output_folder + "\\" + frame_name, img)


def main():
    images_folder = input()
    save_framedata(images_folder, deserialize_framedata(OUTPUT_FILE), "output")


if __name__ == "__main__":
    main()
