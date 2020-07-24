import os
import re


def del_empty_folder(folder_path):
    file_count = 0
    nonempty_folder_count = 0
    for i in os.listdir(folder_path):
        i = os.path.join(folder_path, i)
        if re.match(r"^\.", os.path.basename(i).lower()) and os.path.isfile(i):
            os.remove(i)
            print('删除隐藏文件：', i)
            continue
        if os.path.isfile(i):
            file_count += 1
        if os.path.isdir(i):
            nonempty_folder_count += del_empty_folder(i)
    if file_count == 0 and nonempty_folder_count == 0:
        os.rmdir(folder_path)
        print('删除空目录：', folder_path)
        return 0
    else:
        return 1


if __name__ == "__main__":
    del_empty_folder('/Users/Yo/python/.vscode/')
