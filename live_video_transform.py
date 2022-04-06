import os
import subprocess
from time import sleep

import psutil


def video_transform(input_video_path):
    input_video_path_without_ext = os.path.splitext(input_video_path)[0]
    vtemp_file_path = input_video_path_without_ext + '_vtemp.mp4'
    atemp_file_path = input_video_path_without_ext + '_atemp.aac'
    output_video_path = input_video_path_without_ext + '.mp4'

    video_extract_audio_command = f'ffmpeg -i "{input_video_path}" -vn -sn -c:a copy -y -map 0:a:0 "{atemp_file_path}"'
    print(f"1.运行指令：{video_extract_audio_command}")
    result = subprocess.call(video_extract_audio_command, shell=True)
    print(f"1.运行结果：{result}\n")
    if result != 0:
        return False

    video_convert_command = f'"D:/工具/MarukoToolbox/tools/x264_64-10bit.exe" --crf 24.0 --preset 8  -I 200 -r 4 -b 3 --me umh -i 1 --scenecut 60 -f 1:1 --qcomp 0.5 --psy-rd 0.3:0 --aq-mode 2 --aq-strength 0.8 -o "{vtemp_file_path}" "{input_video_path}"'
    print(f"2.运行指令：{video_convert_command}")
    result = subprocess.call(video_convert_command, shell=True)
    print(f"2.运行结果：{result}\n")
    if result != 0:
        return False

    combine_a_v_command = f'"D:/工具/MarukoToolbox/tools/mp4box.exe" -add "{vtemp_file_path}#trackID=1:name=" -add "{atemp_file_path}#trackID=1:name=" -new "{output_video_path}"'
    print(f"3.运行指令：{combine_a_v_command}")
    result = subprocess.call(combine_a_v_command, shell=True)
    print(f"3.运行结果：{result}\n")
    if result != 0:
        return False

    os.remove(vtemp_file_path)
    os.remove(atemp_file_path)
    return True


def check_idle():
    cpu_usage = []
    psutil.cpu_percent()
    for _ in range(10):
        cpu_usage.append(psutil.cpu_percent(360))
    avg_cpu_usage = sum(cpu_usage) / len(cpu_usage)
    msg = f"过去一个小时平均CPU使用率为{avg_cpu_usage}，"
    if avg_cpu_usage > 80:
        print(msg+"此次任务取消...")
        return False
    else:
        print(msg+"此次任务即将开始...")
        return True


def search_flv_transform(*folder_paths):
    if not check_idle():
        return
    for folder_path in folder_paths:
        folder_path = os.path.abspath(folder_path)
        try:
            for file_name in os.listdir(folder_path):
                if not os.path.splitext(file_name)[-1] == '.flv':
                    continue
                file_abs_file = os.path.join(folder_path, file_name)
                if video_transform(file_abs_file):
                    os.remove(file_abs_file)
        except FileNotFoundError as e:
            print(e, "跳过...")


if __name__ == '__main__':
    search_flv_transform(r"Y:\22128636-OakNose")
