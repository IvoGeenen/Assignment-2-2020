import os
path = "/usr/jquery-data/"
subdirectories = sorted(next(os.walk(path))[1])
subdirectories.sort(key=lambda s: list(map(int, s.split('.'))))
total = (len(subdirectories) * (len(subdirectories)-1))/2
i = 0

for directory1 in subdirectories:
    os.system(f"cloc {path}{directory1}/src --not-match-d=sizzle --json --out=/usr/cloc_output/{directory1}.json")
    for directory2 in subdirectories:
        if directory1 == directory2:
            break
        os.system(f"jsinspect {path}{directory2}/src {path}{directory1}/src -I -L --truncate 1 --ignore 'intro.js|outro.js|sizzle' -r json > /usr/jsinspect_output/{directory2}-{directory1}.json ")
        print(f"{i/total*100}% done")
        i += 1
