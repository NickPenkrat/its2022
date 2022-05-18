import yaml
from FrameData import FrameData

TO_SAVE_DATA = "yaml_files/to_save_data.yaml"


def set_yaml_representer():
    yaml.add_representer(FrameData, yaml_equivalent_of_default)


def yaml_equivalent_of_default(dumper, data):
    dict_representation = data.__dict__
    node = dumper.represent_dict(dict_representation)
    return node


def save_new_data(new_data):
    with open(TO_SAVE_DATA, 'w') as f:
        yaml.dump(new_data, f, default_flow_style=True, sort_keys=False)

    with open(TO_SAVE_DATA, 'r') as f:
        saved_data = yaml.safe_load(f)
    return saved_data


def serialize_new_data(new_data, outfile):
    with open(outfile, 'r') as f:
        data = yaml.safe_load(f)

    data += [save_new_data(new_data)]

    with open(outfile, 'w') as f:
        yaml.dump(data, f, default_flow_style=True, sort_keys=False)


def deserialize_data(outfile, frame_list):
    with open(outfile, 'r') as f:
        file_data = yaml.safe_load(f)
    for dictionary in file_data:
        new_frame = FrameData(dictionary["name"],
                              dictionary["box_count"],
                              dictionary["boxes"])
        frame_list.append(new_frame)
        print(new_frame.name + "deserialized")
