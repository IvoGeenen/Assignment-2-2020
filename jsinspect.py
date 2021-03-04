import os

subdirectories = sorted(next(os.walk("/usr/jquery-data"))[1])
i = 0
for directory1 in subdirectories:
    os.system("cloc " + directory1 + "/src --json --out=/usr/cloc_output/" + directory1 + ".json")
    for directory2 in subdirectories:
        if directory1 == directory2:
            break
        os.system("jsinspect " + directory2 + "/src " + directory1 + "/src -I -L -r json > "
                    "/usr/jsinspect_output/" + directory2 +"-" + directory1 + ".json")