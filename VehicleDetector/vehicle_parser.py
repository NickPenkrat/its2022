import os
import glob
import cv2
from SerializeFrameData import *
from vehicle_detector import VehicleDetector

OUTPUT_FILE = "yaml_files/output.yaml"


def extract_name(input_path_len, image_path):
    return image_path[input_path_len:]


# Extracts image data as dataclass
def get_image_data(image, vehicle_detector, name):
    vehicle_boxes = vehicle_detector.detect_vehicles(image)
    local_rectangles = []

    for box in vehicle_boxes:
        x, y, w, h = box
        local_rectangles.append([int(x), int(y), int(w), int(h)])
        cv2.rectangle(image, (x, y), (x + w, y + h), (25, 0, 180), 2)

    cv2.imwrite('output/' + 'parsed_' + name[:-4] + '.jpg', image)

    return FrameData(name, len(local_rectangles), local_rectangles)


def parse_images(input_path, images_folder, vehicle_detector, outfile_path):
    index = 0
    for image_path in images_folder:
        print("Currently parsing: " + str(image_path))
        image = cv2.imread(image_path)
        frameData = get_image_data(image, vehicle_detector, extract_name(len(input_path) + 1, image_path))
        serialize_new_data(frameData, outfile_path)
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
    parse_images(input_path,
                 images_folder,
                 VehicleDetector(os.environ['YOLO_WEIGHTS'], os.environ['YOLO_CONFIG']),
                 OUTPUT_FILE)


if __name__ == "__main__":
    main()
