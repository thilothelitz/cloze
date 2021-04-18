import sys
import argparse
from enum import Enum
import csv


class Levels(Enum):
    A1 = 1
    A2 = 2
    B1 = 3
    B2 = 4
    C1 = 5

    def __str__(self):
        return self.name


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--levels", type=Levels.__getitem__, choices=Levels, nargs="*")
    parser.add_argument("--min-frequency", type=float)
    parser.add_argument("--tags", nargs="*")
    return parser


if __name__ == "__main__":
    parser = get_argument_parser()
    args = parser.parse_args()

    word_levels = {}
    for row in csv.DictReader(sys.stdin, delimiter="\t"):
        word = row["word"]
        if len(word) <= 1 or not word.isalpha():
            continue
        tag = row["tag"]
        if args.tags is not None and tag not in args.tags:
            continue
        total_frequency = float(row["total_freq@total"])
        if args.min_frequency is not None and total_frequency < args.min_frequency:
            continue

        for level in Levels:
            level_frequency = float(row[f"level_freq@{level.name.lower()}"])
            if level_frequency > total_frequency * 0.8:
                break
        else:
            level = None
        if level is not None:
            if word not in word_levels or word_levels[word].value < level.value:
                word_levels[word] = level

        # print(level.name, word, tag)
        # from matplotlib import pyplot as plt
        # plt.bar(
        #     [level.name for level in Levels],
        #     [float(row[f"level_freq@{level.name.lower()}"]) for level in Levels]
        # )
        # plt.axhline(y=total_frequency, color='red')
        # plt.show()

    for word, level in word_levels.items():
        if args.levels is None or level in args.levels:
            print(word)
