import numpy
from yaml_parser import deserialize_track
from yaml_parser import OUTPUT_TRACK_FILE
import matplotlib
import matplotlib.pyplot as plt

import numpy as np


# Сколько всего машин
# Средняя длина треков
# График: по x -- длина трека, по y -- количество треков с такой длиной

def print_track_storage(track_storage):
    for track in track_storage:
        print("id: " + str(track))
        print("boxes: ")
        for box in track_storage[track]:
            box.print_data()


def main():
    data = deserialize_track(OUTPUT_TRACK_FILE)
    # data = {id -- id car: [box: Box] -- длина листа = трек}
    # print_track_storage(data)
    print(f'Number of cars: {len(data.keys())}')
    lengths = []
    for car in data:
        lengths.append(len(data[car]))
    # print(f'Lengths of paths: {lengths}')
    num_bins = 25
    fig, ax = plt.subplots(dpi=300)
    ax.hist(lengths, num_bins)
    fig.tight_layout()
    ax.set_xlabel('Car trace length')
    ax.set_ylabel('Number of cars')
    ax.set_title('Car trace length distribution')
    # ax.text(max(lengths) * 0.7, 80, f'Number of cars: {len(lengths)}', bbox=dict(facecolor='cyan', alpha=0.25))
    plt.savefig('testplot.png')
    plt.show()


if __name__ == "__main__":
    main()
