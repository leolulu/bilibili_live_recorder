import arrow
import os
import shutil
import re
from video_utility import extract_thumbnail, video_rotate_executer


def daily_take_in(base_dir, rotate_type):
    '''rotate_type只能为"both","metadata","transposed"其中之一
    '''
    if rotate_type not in ['both', 'metadata', 'transposed']:
        raise UserWarning('rotate_type只能为"both","metadata","transposed"其中之一')
    flv_store_folder_name = 'FLVs'
    xml_store_folder_name = 'XMLs'
    os.chdir(base_dir)

    current_task_folder_list = set()
    for i in [i for i in os.listdir(base_dir) if os.path.isfile(i)]:
        if re.match(r".ds", i.lower()):
            os.remove(i)
            continue
        to_folder = arrow.get(i.split('_')[0]).format('YYYY[年]MM[月]DD[日]_dddd', locale='zh')
        current_task_folder_list.add(to_folder)
        if not os.path.exists(to_folder):
            os.mkdir(to_folder)
        shutil.move(i, to_folder)
    if current_task_folder_list:
        print(arrow.now().format(), '本次处理的文件夹：', current_task_folder_list)
    else:
        print(arrow.now().format(), '本次没有新处理...')

    for day_folder in current_task_folder_list:
        os.chdir(os.path.join(base_dir, day_folder))
        for file_in_day in os.listdir('.'):
            if os.path.splitext(file_in_day)[-1] == '.flv':
                if not os.path.exists(flv_store_folder_name):
                    os.mkdir(flv_store_folder_name)
                shutil.move(file_in_day, flv_store_folder_name)
            elif os.path.splitext(file_in_day)[-1] == '.xml':
                if not os.path.exists(xml_store_folder_name):
                    os.mkdir(xml_store_folder_name)
                shutil.move(file_in_day, xml_store_folder_name)
            elif os.path.splitext(file_in_day)[-1] == '.mp4':
                formated_name = arrow.get(file_in_day, 'YYYYMMDD_HHmmss[.mp4]', tzinfo='local')\
                    .format('HH[时]mm[分][.mp4]', locale='zh')
                os.rename(
                    file_in_day,
                    formated_name
                )
                metadata_to_name, transpose_to_name = video_rotate_executer(formated_name, rotate_type)
                extract_thumbnail(metadata_to_name if metadata_to_name is not None else transpose_to_name)


if __name__ == "__main__":
    base_dir = r"C:\LiveRecords\22128636"
    daily_take_in(base_dir, 'metadata')
