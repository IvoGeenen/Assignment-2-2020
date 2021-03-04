import json
from os import listdir

cloc_path = "/usr/cloc_output/"
jsinspect_path = "/usr/jsinspect_output/"

jsinspect_files = listdir(jsinspect_path)

for file in jsinspect_files:

    # Get both versions that are being compared
    version1 = file.split(".json")[0].split("-")[0]
    version2 = file.split(".json")[0].split("-")[1]

    # Load cloc file of both versions
    loc_v1_json = json.load(open(cloc_path + version1 + ".json"))
    loc_v2_json = json.load(open(cloc_path + version2 + ".json"))

    # Get total loc
    loc_v1 = loc_v1_json["JavaScript"]["blank"] + loc_v1_json["JavaScript"]["comment"] + loc_v1_json["JavaScript"]["code"]
    loc_v2 = loc_v2_json["JavaScript"]["blank"] + loc_v2_json["JavaScript"]["comment"] + loc_v2_json["JavaScript"]["code"]

    # Load jsinspect file
    dup_json = json.load(open(jsinspect_path + file))

    dup_loc = 0
    for match in dup_json:
        # Check if the match if from different versions
        if match["instances"][0]["path"] == match["instances"][1]["path"]:
            continue;
        else:
            loc1 = match["instances"][0]["lines"][-1] - match["instances"][0]["lines"][0] + 1
            loc2 = match["instances"][1]["lines"][-1] - match["instances"][1]["lines"][0] + 1

            min_loc = min(loc1, loc2)

            dup_loc += min_loc

    coverage = 2*dup_loc/(loc_v1 + loc_v2)
    print(f"file: {file}, coverage: {coverage}")






