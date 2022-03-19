import os
import shutil


def recursive_search_source_folder(source_folder_path, target_folder_path):
    messages = list()

    def print_(*arg):
        print(arg)
        for msg in arg:
            messages.append(msg)

    source_folder_path = os.path.abspath(source_folder_path)
    target_folder_path = os.path.abspath(target_folder_path)
    os.chdir(source_folder_path)
    for dir_, folders, files in os.walk('.'):
        for folder in folders:
            folder_ = os.path.join(target_folder_path, dir_, folder)
            os.mkdir(folder_)
            print_(f"创建目标文件夹：{folder_}")
        for file in files:
            s_file_ = os.path.join(dir_, file)
            d_file_ = os.path.join(target_folder_path, dir_, file)
            print_(f"复制原文件【{s_file_}】到目标文件【{d_file_}】")
            copy_result = False
            retry_times = 5
            while (not copy_result) and (retry_times > 0):
                copy_result = copy_file_with_verify(s_file_, d_file_)
                if not copy_result:
                    retry_times -= 1
                    print_(f"复制失败，重试次数：{retry_times}")
            if retry_times == 0:
                print_("这个文件复制失败了！！！")
            else:
                print_("复制成功，校验成功")

    return messages


def copy_file_with_verify(source_path, target_path):
    shutil.copyfile(source_path, target_path)
    if os.path.getsize(source_path) == os.path.getsize(target_path):
        return True
    else:
        return False


if __name__ == '__main__':
    recursive_search_source_folder(
        r"E:\fuck\New folder\源",
        r"E:\fuck\New folder\目标"
    )
