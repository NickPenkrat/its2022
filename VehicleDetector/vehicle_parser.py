import os
import glob
import cv2
from SerializeFrameData import *
from TrackBuilder import TrackBuilder
from vehicle_detector import VehicleDetector

OUTPUT_FILE = "yaml_files/output.yaml"


def extract_name(input_path_len, image_path):
    return image_path[input_path_len:]


def write_objects(image, framedata):
    for i in range(framedata.box_count):
        org = (framedata.boxes[i][0], framedata.boxes[i][1])
        cv2.putText(image, framedata.box_objects[i].get_id(), org, cv2.FONT_HERSHEY_SIMPLEX, 1, (25, 0, 180))


# Extracts image data as dataclass
def get_image_data(image, vehicle_detector, name, previous_frame, trackbuilder):
    vehicle_boxes = vehicle_detector.detect_vehicles(image)
    local_rectangles = []

    for box in vehicle_boxes:
        x, y, w, h = box
        if int(w) * int(h) >= 300:
            local_rectangles.append([int(x), int(y), int(w), int(h)])
            cv2.rectangle(image, (x, y), (x + w, y + h), (25, 0, 180), 2)

    framedata = FrameData(name, len(local_rectangles), local_rectangles)
    if previous_frame is None:
        trackbuilder.build_track(framedata)
    else:
        trackbuilder.build_track(framedata, previous_frame)
    write_objects(image, framedata)
    cv2.imwrite('output/' + 'parsed_' + name[:-4] + '.jpg', image)
    return framedata


def parse_images(input_path, images_folder, vehicle_detector, outfile_path, trackbuilder):
    index = 0
    previous_frame = None
    for image_path in images_folder:
        print("Currently parsing: " + str(image_path))
        image = cv2.imread(image_path)
        frameData = get_image_data(image,
                                   vehicle_detector,
                                   extract_name(len(input_path) + 1, image_path),
                                   previous_frame,
                                   trackbuilder)
        serialize_new_data(frameData, outfile_path)
        previous_frame = frameData
        index += 1


# Deserializes data from yaml
def parse_yaml(outfile):
    deserialized_data = []
    deserialize_data(outfile, deserialized_data)


# Input path to "images" folder
def main():
    input_path = input()
    images_folder = glob.glob(input_path + "/*.png")
    set_yaml_representer()
    trackbuilder = TrackBuilder()
    parse_images(input_path,
                 images_folder,
                 VehicleDetector(os.environ['YOLO_WEIGHTS'], os.environ['YOLO_CONFIG']),
                 OUTPUT_FILE,
                 trackbuilder)


if __name__ == "__main__":
    main()
