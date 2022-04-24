import os
import csv
from collections import defaultdict


def read_folder_recursively(root):
    all_files = []
    for root, subdirs, files in os.walk(root):
        for file in files:
            all_files.append(os.path.join(root, file))
        for subdir in subdirs:
            all_files.extend(read_folder_recursively(os.path.join(root, subdir)))
        if not subdirs:
            break
    return all_files


def create_unique_blocks_csv(root_dir, csv_dir):
    unique_bbs = defaultdict(lambda: 0)
    all_bb_files = [f for f in read_folder_recursively(root_dir) if "_bbs" in f]
    for filename in all_bb_files:
        with open(filename) as f:
            all_bbs = f.read().split("\n\n")

        all_bbs = [bb.replace("\n", "") for bb in all_bbs]
        for bb in all_bbs:
            unique_bbs[bb] += 1

    with open(os.path.join(csv_dir, "unique_blocks.csv"), "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["BB", "#"])
        for key, value in unique_bbs.items():
            writer.writerow([key, value])


def generate_random_vector(size, gf):
    return gf.Random(size).tolist()


if __name__ == '__main__':
    bbs_dir = r'C:\Users\User\Dropbox\CFI Project\Robust_CFC_Paper\Implementation\Software\Final\dump'
    csv_dir = r'C:\Users\User\PycharmProjects\robust_cfc'
    create_unique_blocks_csv(bbs_dir, csv_dir)
