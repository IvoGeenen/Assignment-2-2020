import json
from os import listdir, path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

cloc_path = "/usr/cloc_output/"
jsinspect_path = "/usr/jsinspect_output/"
output_path = "/out/"

# Function for retrieving the ordered list of jsinspect files
def get_ordered_jsinspect_files():
    # Get all files from the jsinspect directory
    all_files = [path.splitext(filename)[0] for filename in listdir(jsinspect_path)]

    # Construct a set with all diferent version labels
    all_labels = set()
    for file in all_files:
        all_labels.add(file.split("-")[0])
        all_labels.add(file.split("-")[1])

    # Convert the set of labels to a list and sort them
    labels = list(all_labels)
    labels.sort(key=lambda s: list(map(int, s.split('.'))))

    # Construct the ordered list of files from the labels
    file_list = []
    for idx, l1 in enumerate(labels):
        counter = idx + 1
        for l2 in labels:
            if counter > 0:
                counter -= 1
                continue
            else:
                file_list.append(l1 + "-" + l2)

    return file_list, labels

# Function for calculating the coverage of a file
def calculate_coverage(file):
    # Get both versions that are being compared
    version1 = file.split("-")[0]
    version2 = file.split("-")[1]

    # Load cloc file of both versions
    loc_v1_json = json.load(open(cloc_path + version1 + ".json"))
    loc_v2_json = json.load(open(cloc_path + version2 + ".json"))

    # Get loc of both files
    loc_v1 = loc_v1_json["header"]["n_lines"]
    loc_v2 = loc_v2_json["header"]["n_lines"]

    # Load jsinspect file
    jsinspect_json = json.load(open(jsinspect_path + file + ".json"))

    dup_loc = 0
    dup_intervals = []
    # Loop over all matches in the file
    for match in jsinspect_json:
        for inst in match["instances"]:
            path = inst["path"]
            lines = inst["lines"]
            contains = False
            # Check if there is already an match for this file, if so add the interval to it, otherwise create new
            for dup in dup_intervals:
                if path in dup:
                    dup[1].append(lines)
                    contains = True
                    break
            if not contains:
                dup_intervals.append([path, [lines]])

    # Sort the intervals
    for interval_list in dup_intervals:
        interval_list[1].sort()

    # Construct list with only the intervals (i.e. without "path")
    only_intervals = []
    for interval in dup_intervals:
        only_intervals.append(interval[1])

    # Merge overlapping intervals together such that they are not counted twice
    merged_intervals = []
    for interval in only_intervals:
        merged = [interval[0]]
        for current in interval:
            previous = merged[-1]
            if current[0] <= previous[1]:
                previous[1] = max(previous[1], current[1])
            else:
                merged.append(current)
        merged_intervals.append(merged)

    # Calculate the lines of duplicate code from the intervals
    for interval_list in merged_intervals:
        for interval in interval_list:
            dup_loc += interval[1] - interval[0] + 1

    # Calculate coverage
    coverage = dup_loc / (loc_v1 + loc_v2)

    return coverage


# Function for constructing the matrix
def construct_matrix(size: int, coverage_list):
    # Initialize a matrix with all zeros
    matrix = np.zeros((size, size))

    # Fill in the values at the right spot in the matrix
    cov_counter = 0
    for i in range(size):
        counter = i + 1

        for j in range(size):
            if counter > 0:
                counter -= 1
                continue
            else:
                matrix[j][i] = coverage_list[cov_counter]
                cov_counter += 1
    return matrix

# Function for drawing the heatmap
def draw_heatmap(matrix):
    # Create a mask for the upper half of the heatmap
    mask = np.zeros_like(matrix)
    mask[np.triu_indices_from(mask)] = True

    # Declare figure size and create heatmap
    fig, ax = plt.subplots(figsize=(15, 20))
    ax = sns.heatmap(matrix, vmin=0, vmax=1, cmap="YlGnBu",
                     xticklabels=labels, yticklabels=labels,
                     linewidths=0.01, linecolor='grey', mask=mask, cbar_kws={"orientation": "horizontal"})

    # Save the heatmap
    fig.savefig(f"{output_path}/heatmap.png", dpi=400)


if __name__ == "__main__":
    # Get all jsinspect files and all ordered labels
    print("Retrieving all files...")
    jsinspect_files, labels = get_ordered_jsinspect_files()

    # Calculate the coverage for every file
    print("Calculating coverages...")
    coverage_list = []
    for idx, file in enumerate(jsinspect_files):
        if idx % 500 == 0:
            print(f"{idx/len(jsinspect_files)*100}% done")
        coverage_list.append(calculate_coverage(file))
    print("100% done")

    # Construct the matrix from the coverage list
    print("Constructing matrix...")
    coverage_matrix = construct_matrix(len(labels), coverage_list)

    # Draw and save the heatmap from the matrix
    print("Drawing heatmap...")
    draw_heatmap(coverage_matrix)
    print("Finished")
