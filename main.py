import os.path
from os import listdir
from os.path import isfile, join
from functools import cmp_to_key


def is_valid_type(mypath):
    file = mypath.split(".")

    if len(file) < 2:
        return False

    if '\\node_modules\\' in mypath:
        return False
    if 'git\\objects\\' in mypath:
        return False
    if 'AppData\\Local\\' in mypath:
        return False
    if '.vscode\\extensions\\' in mypath:
        return False
    if 'AppData\\Roaming\\' in mypath:
        return False

    file_extension = file[len(file) - 1]

    if file_extension == "ts" or file_extension == 'tsx':
        return True
    return False


def filter_files(only_files, mypath):
    if len(only_files) < 1:
        return []

    result_filter = []
    for f in only_files:
        p = os.path.join(mypath, f)
        if is_valid_type(p):
            result_filter.append(p)

    return result_filter


def explore(mypath, level=1):
    result_explore = []
    only_files = []
    try:
        only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    except:
        pass

    only_files_good = filter_files(only_files, mypath)
    only_dirs = []
    try:
        only_dirs = [f for f in listdir(mypath) if os.path.isdir(join(mypath, f))]
    except:
        pass

    if len(only_files_good) > 0:
        # print("Explore level " + str(level))
        # print(only_files_good)
        for file_good in only_files_good:
            try:
                num_lines = sum(1 for _ in open(file_good))
                dict_explore = {"num_lines": num_lines, "file_path": file_good}
                result_explore.append(dict_explore)
            except:
                pass

    for dirFound in only_dirs:
        path = os.path.join(mypath, dirFound)
        subresult = explore(path, level + 1)
        for subresult_value in subresult:
            result_explore.append(subresult_value)

    return result_explore


def compare_lines(item1, item2):
    if item1["num_lines"] > item2["num_lines"]:
        return -1
    elif item1["num_lines"] < item2["num_lines"]:
        return 1
    else:
        if item1["file_path"] < item2["file_path"]:
            return -1
        elif item1["file_path"] > item2["file_path"]:
            return 1
        else:
            return 0


def sort_explore(to_sort):
    to_sort.sort(key=cmp_to_key(compare_lines))
    return to_sort


base_dir = './../../../../'

print("Started with base dir " + str(base_dir))

result = explore(base_dir)
# print("----")
# print(result)

sorted_result = sort_explore(result)
# print("----")
# print(sorted_result)

# print("----")
for item in sorted_result:
    print(item)
