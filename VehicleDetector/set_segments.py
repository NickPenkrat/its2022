import cv2
from track_matching import deserialize_partial_track


def crop_image(img, rect):
    return img[rect.y:rect.y + rect.h, rect.x:rect.x + rect.w]


def set_segments(tracks, images_path, number):
    for obj in tracks:
        first_box = tracks[obj]
        if first_box.rectangle.area < 40000:
            continue
        img = cv2.imread(images_path + "\\" + first_box.frame)
        segment = crop_image(img, first_box.rectangle)
        print(f"Saving segment of {first_box.object_id}")
        cv2.imwrite("output_segments"
                    + str(number) + "/"
                    + str(first_box.object_id)
                    + "_" + first_box.frame[:-3]
                    + 'jpg',
                    segment)


def main():
    track_storage = input("Input track storage: ")
    images_path = input("Input images path: ")
    number = input("Input number of camera (0 or 1): ")
    set_segments(deserialize_partial_track(track_storage), images_path, number)


if __name__ == "__main__":
    main()
