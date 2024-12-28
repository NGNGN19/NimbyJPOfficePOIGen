import csv
import re
from collections import defaultdict
import os
import nimby
import argparse


def wrapped_up(toread_path:str,dir_name,**kwargs):
    toread_col = ['lon', 'lat', 'color', 'text', 'font_size', 'max_lod', 'transparent', 'demand', 'population']
    toread_list = nimby.read_from_tsv(toread_path, toread_col)
    towrite_list = []
    todict1 = {'lon': 'lon',
               'lat': 'lat',
               'color': 'color',
               'text': 'text',
               'font_size': 'font_size',
               'max_lod': 'max_lod',
               'transparent': 'transparent',
               'demand': 'demand',
               'population': 'population'}
    towrite_list.append(todict1)

    classified_data = defaultdict(list)
    pattern = re.compile(r"^(.*?)(?:\d+|[０-９]+)?(丁目|丁)?$")

    for item in toread_list:
        if item['text'] == 'text':
            continue
        match = pattern.match(item['text'])
        if match:
            key = match.group(1)  # 提取共同部分作为分类键
            classified_data[key].append(item)

        # 打印分类结果
    for key, values in classified_data.items():
        lon_store = float(0)
        lat_store = float(0)
        pop_store = int(0)
        count = int(0)
        todict = {'lon': 0,
                  'lat': 0,
                  'color': kwargs['g_color'],
                  'text': key,
                  'font_size': 0,
                  'max_lod': 0,
                  'transparent': 1,
                  'demand': "default",
                  'population': 0}
        for items in values:
            lon_store = lon_store + float(items['lon'])
            lat_store = lat_store + float(items['lat'])
            if items['population'] == '-':
                items['population'] = int(0)
            pop_store = pop_store + int(items['population'])
            count = count + 1
        if kwargs['g_filter'] and pop_store < kwargs['g_filter']:
            continue
        todict['lon'] = round(lon_store / count, 7)
        todict['lat'] = round(lat_store / count, 7)
        todict['population'] = pop_store
        towrite_list.append(todict)
    # print(towrite_list)
    to_write_col = ['lon', 'lat', 'color', 'text', 'font_size', 'max_lod', 'transparent', 'demand', 'population']
    basename = os.path.basename(toread_path)
    nimby.write_to_tsv(f"mod/KM_{kwargs['g_prefix']}POI_{dir_name}/{kwargs['g_prefix']}{basename}", to_write_col, towrite_list)

def write_gappei_mod(source_path,target_path):
    old_string = "KM_"
    new_string = "Simp_KM_"
    str2 = 'Hiring Data'
    str2n = 'Simpler Hiring Data'
    with open(source_path, "r", encoding="utf-8") as f_src:
        with open(target_path, "w", encoding="utf-8") as f_dst:
            for line in f_src:
                modified_line = line.replace(str2, str2n)
                modified_line = modified_line.replace(old_string, new_string)
                f_dst.write(modified_line)

def gappei(city_name:str,**kwargs):
    inner_name_list, city_name_list=nimby.read_name_list(city_name)
    inner_name = inner_name_list['en']
    directory = f"mod/KM_POI_{inner_name}/"
    nimby.write_mod_txt(inner_name_list,city_name_list,mod_prefix=kwargs['g_prefix'],**kwargs)
    # 遍历目录中的文件
    for filename in os.listdir(directory):
        # 检查文件名是否符合特定的结构，例如以 "file" 开头并且以 ".txt" 结尾
        if filename.startswith(f'KM_{inner_name}') and filename.endswith(".tsv"):
            filepath = f'{directory}{filename}'
            #print(f'Wrapping {os.path.basename(filepath)}')
            wrapped_up(filepath,inner_name,**kwargs)
    #write_gappei_mod(f'{directory}/mod.txt',mod_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter the name of the list using --name')
    parser.add_argument('--name',type=str,help='name of the list',required=True)
    parser.add_argument('--color',type=str,default='ff0000')
    parser.add_argument('--g_filter',type=int)
    parser.add_argument('--g_prefix',default='Simp_')
    args = parser.parse_args()
    args_dict = vars(args)

    pref_name = args.name
    gappei(pref_name,**args_dict)

