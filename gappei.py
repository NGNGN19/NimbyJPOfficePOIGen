import csv
import re
from collections import defaultdict
import os


def write_to_tsv(output_path: str, file_columns: list, data: list):
    csv.register_dialect('tsv_dialect', delimiter='\t', quoting=csv.QUOTE_NONE)
    with open(output_path, "w", newline="",encoding="utf8") as wf:
        writer = csv.DictWriter(wf, fieldnames=file_columns, dialect='tsv_dialect')
        writer.writerows(data)
    csv.unregister_dialect('tsv_dialect')


def read_from_csv(file_path: str, column_names: list) -> list:
    csv.register_dialect('csv_dialect', delimiter=',', quoting=csv.QUOTE_ALL)
    with open(file_path, "r",encoding="utf8") as wf:
        reader = csv.DictReader(wf, fieldnames=column_names, dialect='csv_dialect')
        datas = []
        for row in reader:
            data = dict(row)
            datas.append(data)
    csv.unregister_dialect('csv_dialect')
    return datas


def read_from_tsv(file_path: str, column_names: list) -> list:
    csv.register_dialect('tsv_dialect', delimiter='\t', quoting=csv.QUOTE_ALL)
    with open(file_path, "r",encoding="utf8") as wf:
        reader = csv.DictReader(wf, fieldnames=column_names, dialect='tsv_dialect')
        datas = []
        for row in reader:
            data = dict(row)
            datas.append(data)
    csv.unregister_dialect('tsv_dialect')
    return datas


def wrapped_up(toread_path:str):
    toread_col = ['lon', 'lat', 'color', 'text', 'font_size', 'max_lod', 'transparent', 'demand', 'population']
    toread_list = read_from_tsv(toread_path, toread_col)
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
    pattern = re.compile(r"^[^\d１２３４５６７８９丁目]+")

    for item in toread_list:
        if item['text'] == 'text':
            continue
        match = pattern.match(item['text'])
        if match:
            key = match.group(0)  # 提取共同部分作为分类键
            classified_data[key].append(item)

        # 打印分类结果
    for key, values in classified_data.items():
        lon_store = float(0)
        lat_store = float(0)
        pop_store = int(0)
        count = int(0)
        todict = {'lon': 0,
                  'lat': 0,
                  'color': '000000',
                  'text': key,
                  'font_size': 0,
                  'max_lod': 0,
                  'transparent': 1,
                  'demand': "KM_Office",
                  'population': 0}
        for items in values:
            lon_store = lon_store + float(items['lon'])
            lat_store = lat_store + float(items['lat'])
            if items['population'] == '-':
                items['population'] = int(0)
            pop_store = pop_store + int(items['population'])
            count = count + 1
        todict['lon'] = lon_store / count
        todict['lat'] = lat_store / count
        todict['population'] = pop_store
        towrite_list.append(todict)
    # print(towrite_list)
    to_write_col = ['lon', 'lat', 'color', 'text', 'font_size', 'max_lod', 'transparent', 'demand', 'population']
    basename = os.path.basename(toread_path)
    write_to_tsv(f"data/{city_name}/Simp_{basename}", to_write_col, towrite_list)


city_name = input('Input name:')
# ward_name = 'Chiyoda'
# ward_name = input('Input name:')
# toread_path = f"data/{city_name}/KM_{city_name}_{ward_name}.tsv"
directory = f"data/{city_name}/"

# 遍历目录中的文件
for filename in os.listdir(directory):
    # 检查文件名是否符合特定的结构，例如以 "file" 开头并且以 ".txt" 结尾
    if filename.startswith(f'KM_{city_name}') and filename.endswith(".tsv"):
        wrapped_up(f'{directory}{filename}')

