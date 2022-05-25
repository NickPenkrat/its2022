from SerializeFrameData import *


# Deserializes data from yaml
def parse_yaml(file_path, deserialized_data):
    deserialize_data(file_path, deserialized_data)


def main():
    file_path = input()
    deserialized_data = []
    parse_yaml(file_path, deserialized_data)


if __name__ == "__main__":
    main()
