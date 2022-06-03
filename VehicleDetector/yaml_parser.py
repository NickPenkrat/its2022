import glob
import yaml
from Rectangle import Rectangle
from FrameData import FrameData
from Box import Box
from TrackBuilder import TrackBuilder

OUTPUT_TRACK_FILE = "yaml_files/output_track_storage.yaml"
OUTPUT_FILE = "yaml_files/output.yaml"
TO_SAVE_DATA = "yaml_files/to_save_data.yaml"
MINIMAL_AREA = 300


def set_yaml_representer():
    yaml.add_representer(FrameData, yaml_equivalent_of_default)
    yaml.add_representer(Box, yaml_equivalent_of_default)
    yaml.add_representer(Rectangle, yaml_equivalent_of_default)


def yaml_equivalent_of_default(dumper, data):
    dict_representation = data.__dict__
    node = dumper.represent_dict(dict_representation)
    return node


def extract_name(yaml_file, input_folder):
    name = yaml_file[len(input_folder) + 1:-4] + ".png"
    return name.replace("_", "-")


def serialize_data(data, outfile):
    with open(outfile, 'w') as f:
        yaml.dump(data, f, default_flow_style=True, sort_keys=False)


def deserialize_frame(yaml_file, frame_number, input_folder):
    skip_lines = 2
    with open(yaml_file) as infile:
        for i in range(skip_lines):
            _ = infile.readline()
        data = yaml.safe_load(infile)

    boxes = []
    frame_name = extract_name(yaml_file, input_folder)
    for item in data["boxes"]:
        rectangle = Rectangle([
            item["x_min"],
            item["y_min"],
            item["x_max"] - item["x_min"],
            item["y_max"] - item["y_min"]
        ])
        if rectangle.area < MINIMAL_AREA:
            continue
        box = Box(item["id"],
                  item["conf"],
                  item["class"],
                  rectangle,
                  frame_name)
        boxes.append(box)
    framedata = FrameData(frame_number, frame_name, len(boxes), boxes)
    return framedata


def parse_frame_data(yaml_folder, trackbuilder, input_folder):
    framedata_storage = []
    parse_later = []
    index = 0
    previous_framedata = None
    for yaml_file in yaml_folder:
        if "frame_1" in yaml_file:
            parse_later.append(yaml_file)
            continue
        print("Currently parsing: " + yaml_file)
        framedata = deserialize_frame(yaml_file, index, input_folder)
        framedata = trackbuilder.build_track(framedata, previous_framedata)
        framedata_storage.append(framedata)
        previous_framedata = framedata
        index += 1
    for yaml_file in parse_later:
        print("Currently parsing: " + yaml_file)
        framedata = deserialize_frame(yaml_file, index, input_folder)
        framedata = trackbuilder.build_track(framedata, previous_framedata)
        framedata_storage.append(framedata)
        previous_framedata = framedata
        index += 1
    return framedata_storage


def serialize_track_storage(trackbuilder, outfile):
    with open(outfile, 'w') as f:
        yaml.dump(trackbuilder.to_serialize(), f)


def deserialize_track(outfile):
    track_storage = {}
    with open(outfile, 'r') as f:
        data = yaml.safe_load(f)
    for key in data.keys():
        boxes = []
        for item in data[key]:
            rectangle = Rectangle([
                item["rectangle"]["x"],
                item["rectangle"]["y"],
                item["rectangle"]["w"],
                item["rectangle"]["h"]
            ])
            box = Box(item["id"],
                      item["conf"],
                      item["class"],
                      rectangle,
                      item["frame"])
            boxes.append(box)
        track_storage[key] = boxes
    return track_storage


def main():
    set_yaml_representer()
    input_folder = input()
    trackbuilder = TrackBuilder()
    yaml_folder = glob.glob(input_folder + "/*.yml")
    framedata_storage = parse_frame_data(yaml_folder, trackbuilder, input_folder)
    serialize_data(framedata_storage, OUTPUT_FILE)
    serialize_track_storage(trackbuilder, OUTPUT_TRACK_FILE)
    print("All parsed")


if __name__ == "__main__":
    main()
