import glob
import numpy as np
import yaml
from MatchPairsData import MatchPairsData
from Rectangle import Rectangle
from Box import Box
from save_data import save_framedata
from save_data import deserialize_framedata
from yaml_parser import serialize_data


def parse_npz(path):
    npz = np.load(path)
    return MatchPairsData(npz['keypoints0'],
                          npz['keypoints1'],
                          npz['matches'],
                          npz['match_confidence'])


def find_keypoints_in_box(box, keypoint_array):
    rectangle = Rectangle(box)
    keypoints_in_box = []
    keypoints_indexes = []
    for i in range(len(keypoint_array)):
        keypoint = keypoint_array[i]
        if rectangle.x <= int(keypoint[0]) <= rectangle.x + rectangle.w:
            if rectangle.y <= int(keypoint[1]) <= rectangle.y + rectangle.h:
                keypoints_in_box.append([int(keypoint[0]), int(keypoint[1])])
                keypoints_indexes.append(i)
    return keypoints_in_box, keypoints_indexes


def find_matches(keypoints0, matches):
    matching_keypoints = 0
    for i in range(len(keypoints0)):
        if matches[i] != -1:
            matching_keypoints += 1
    return matching_keypoints


def is_in_box(box, keypoint):
    rectangle = Rectangle(box)
    if rectangle.x <= int(keypoint[0]) <= rectangle.x + rectangle.w:
        if rectangle.y <= int(keypoint[1]) <= rectangle.y + rectangle.h:
            return True
    return False


def find_box(boxes, matching_keypoints):
    max_keypoints = 0
    result_box_index = None
    for i in range(len(boxes)):
        box = boxes[i]
        count = 0
        for keypoint in matching_keypoints:
            if is_in_box(box, keypoint):
                count += 1
        if count > max_keypoints:
            max_keypoints = count
            result_box_index = i
    return result_box_index


def extract_object_id(npz_path, npz_folder_len):
    npz_name = npz_path[npz_folder_len + 1:]
    _, second_part = npz_name.split("__")
    obj_id, _ = second_part.split("_")
    return int(obj_id)


def are_objects_similar(keypoints0, keypoints1, matches, th=0.25):
    min_keypoints = min(keypoints0, keypoints1)
    return matches / min_keypoints >= th


def match_tracks(npz_path, track0):
    matched_tracks = dict()
    for key0 in track0:
        print(f"Parsing object {key0}")
        npz_key0 = glob.glob(npz_path + f"/{str(key0)}_*")
        max_matches = 0
        max_matching_key = None
        for npz in npz_key0:
            key1 = extract_object_id(npz, len(npz_path))
            print(f". . . Comparing with {key1}")
            matchPairsData = parse_npz(npz)
            matches = find_matches(matchPairsData.keypoints0, matchPairsData.matches)
            if matches > max_matches and are_objects_similar(
                    len(matchPairsData.keypoints0),
                    len(matchPairsData.keypoints1),
                    matches):
                max_matches = matches
                max_matching_key = key1
        if max_matching_key is not None:
            is_key_used = matched_tracks.get(max_matching_key)
            if is_key_used is None:
                matched_tracks[max_matching_key] = [key0, max_matches]
            else:
                if max_matches > matched_tracks[max_matching_key][1]:
                    matched_tracks[max_matching_key] = [key0, max_matches]
    print("All parsed")
    return matched_tracks


def change_objects(full_track0, matched_tracks):
    print("Changing objects...")
    for key1 in matched_tracks:
        key0 = matched_tracks[key1][0]
        full_track0[key1] = full_track0.pop(key0)
        print(f"Object {key0} is equal to object {key1}")


def deserialize_partial_track(outfile):
    print("Deserializing track data...")
    track_storage = {}
    with open(outfile, 'r') as f:
        data = yaml.safe_load(f)
    for key in data.keys():
        max_area = 0
        max_box = None
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
            if rectangle.area > max_area:
                max_area = rectangle.area
                max_box = box
        track_storage[key] = max_box
    return track_storage


def change_framedata(framedata_storage1, matched_tracks):
    print("Changing framedata...")
    for framedata1 in framedata_storage1:
        for box in framedata1.boxes:
            obj_id = box.object_id
            to_change = matched_tracks.get(obj_id)
            if to_change is not None:
                box.change_id(matched_tracks[obj_id][0])


def main():
    tracks_path0 = input("Input path to tracks from first camera: ")
    images_path1 = input("Input path to images from second camera: ")
    framedata_storage1_path = input("Input path to framedata from second camera: ")
    npz_files = input("Input path to npz files with matches: ")
    track0 = deserialize_partial_track(tracks_path0)
    framedata_storage1 = deserialize_framedata(framedata_storage1_path)
    matched_tracks = match_tracks(npz_files, track0)
    change_framedata(framedata_storage1, matched_tracks)
    serialize_data(framedata_storage1, "yaml_files/output_matched.yaml")
    save_framedata(images_path1, framedata_storage1, "output/")


if __name__ == "__main__":
    main()
