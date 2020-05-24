import subprocess
import os


def video_rotate_metadata_ver(video_path):
    to_name = '_metadated'.join(os.path.splitext(video_path))
    command = 'ffmpeg -i "{}" -codec copy -metadata:s:v:0 rotate=90 "{}"'
    command = command.format(video_path, to_name)
    print(command)
    subprocess.call(command, shell=True)
    return to_name


def video_rotate_transpose_ver(video_path):
    to_name = '_transposed'.join(os.path.splitext(video_path))
    command = 'ffmpeg -i "{}" -vf "transpose=2" -acodec copy "{}"'
    command = command.format(video_path, to_name)
    print(command)
    subprocess.call(command, shell=True)
    return to_name


def video_rotate_executer(video_path, rotate_type):
    if rotate_type in ['both', 'metadata']:
        metadata_to_name = video_rotate_metadata_ver(video_path)
    if rotate_type in ['both', 'transposed']:
        transpose_to_name = video_rotate_transpose_ver(video_path)
    # 以下两句试跑期间先不开启
    # os.remove(video_path)
    # os.rename(to_name, video_path)
    if rotate_type == 'metadata':
        os.rename(video_path, '_org'.join(os.path.splitext(video_path)))
        os.rename(metadata_to_name, video_path)
        metadata_to_name = video_path
    return (metadata_to_name if 'metadata_to_name' in dir() else None,
            transpose_to_name if 'transpose_to_name' in dir() else None)


def extract_thumbnail(video_path):
    output_pic_name = os.path.splitext(os.path.basename(video_path))[0] + '_thumbnail.jpg'
    command = 'ffmpeg -i "{}" -vframes 1 "{}"'
    command = command.format(video_path, output_pic_name)
    print(command)
    subprocess.call(command, shell=True)
