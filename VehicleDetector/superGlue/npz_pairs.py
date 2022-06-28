import glob
import os
import cv2
from match_pairs import main as run_superglue
from numba import jit


def extract_name(image_path, input_folder_len):
    return image_path[input_folder_len + 1:-4]

@jit
def get_npz_file(image_path1, image_path2, input_folder1_len, input_folder2_len):
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)
    cv2.imwrite("assets\\scannet_sample_images\\1.jpg", img1)
    cv2.imwrite("assets\\scannet_sample_images\\2.jpg", img2)
    run_superglue()
    npz_path = "dump_match_pairs\\1_2_matches.npz"
    img1_name = extract_name(image_path1, input_folder1_len)
    img2_name = extract_name(image_path2, input_folder2_len)
    os.rename(npz_path, "dump_match_pairs\\" + img1_name + "__" + img2_name + ".npz")


def parse_pairs(input_folder1, input_folder2, input1, input2):
    for image_path1 in input_folder1:
        for image_path2 in input_folder2:
            get_npz_file(image_path1, image_path2, input1, input2)


def main():
    input1 = input()
    input2 = input()
    input_folder1 = glob.glob(input1 + "/*.jpg")
    input_folder2 = glob.glob(input2 + "/*.jpg")
    parse_pairs(input_folder1, input_folder2, len(input1), len(input2))


if __name__ == "__main__":
    main()
