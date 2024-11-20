import csv
import json
import overpy
import pandas as pd
import os
import argparse
from zenkaku_replace import zenkaku_replace
import gappei


def write_to_tsv(output_path: str, file_columns: list, data: list):
    csv.register_dialect('tsv_dialect', delimiter='\t', quoting=csv.QUOTE_NONE)
    with open(output_path, "w", newline="",encoding="utf8") as wf:
        writer = csv.DictWriter(wf, fieldnames=file_columns, dialect='tsv_dialect')
        writer.writerows(data)
    csv.unregister_dialect('tsv_dialect')


def read_from_csv(file_path: str, column_names: list) -> list:
    csv.register_dialect('csv_dialect', delimiter=',', quoting=csv.QUOTE_ALL)
    with open(file_path, "r",encoding="utf-8-sig") as wf:
        reader = csv.DictReader(wf, fieldnames=column_names, dialect='csv_dialect')
        datas = []
        for row in reader:
            data = dict(row)
            datas.append(data)
    csv.unregister_dialect('csv_dialect')
    return datas


def read_from_tsv(file_path: str, column_names: list) -> list:
    csv.register_dialect('tsv_dialect', delimiter='\t', quoting=csv.QUOTE_ALL)
    with open(file_path, "r",encoding="utf-8-sig") as wf:
        reader = csv.DictReader(wf, fieldnames=column_names, dialect='tsv_dialect')
        datas = []
        for row in reader:
            data = dict(row)
            datas.append(data)
    csv.unregister_dialect('tsv_dialect')
    return datas


def combine_pop_loc(name_c, name_w):
        loc_path = f"data/{name_c['en']}/{name_c['en']}_{name_w['en']}_loc.tsv"
        pop_path = f"data/{name_c['en']}/{name_c['en']}_{name_w['en']}_pop.tsv"
        loc_col = ["lon", "lat", "name"]
        loc_read = read_from_tsv(loc_path, loc_col)
        # print(loc_read)
        pop_col = ["name", "population"]
        pop_read = read_from_tsv(pop_path, pop_col)
        # print(pop_read)
        to_write = []
        todict1 = {'lon': 'lon',
                   'lat': 'lat',
                   'color': 'color',
                   'text': 'text',
                   'font_size': 'font_size',
                   'max_lod': 'max_lod',
                   'transparent': 'transparent',
                   'demand': 'demand',
                   'population': 'population'}
        to_write.append(todict1)

        for loc_item in loc_read:
            for pop_item in pop_read:
                #zenkaku_replace(loc_item)
                if loc_item["name"] == pop_item['name']:
                    todict = {'lon': 0,
                              'lat': 0,
                              'color': '000000',
                              'text': '',
                              'font_size': 0,
                              'max_lod': 0,
                              'transparent': 1,
                              'demand': "default",
                              'population': 0}
                    todict['text'] = loc_item['name']
                    todict['lon'] = loc_item['lon']
                    todict['lat'] = loc_item['lat']
                    if pop_item['population'] == '-':
                        todict['population'] = 0
                    else:
                        todict['population'] = pop_item['population']
                    to_write.append(todict)

        to_write_col = ['lon', 'lat', 'color', 'text', 'font_size', 'max_lod', 'transparent', 'demand', 'population']
        write_to_tsv(f"mod/KM_POI_{name_c['en']}/KM_{name_c['en']}_{name_w['en']}.tsv",
                     to_write_col, to_write)


# city_name = 'Kawasaki'
# ward_name = 'Chiyoda'
# ward_name = input('Input name:')
# ward_name_list = ['Tsurumi','Kanagawa','Nishi','Naka','Minami','Hodogaya','Isogo',
#                   'Kanazawa','Kohoku','Totsuka','Konan','Asahi','Midori','Seya',
#                   'Sakae','Izumi','Aoba','Tsuzuki']
# ward_name_list = ['Kawasaki',"Saiwai","Nakahara",'Takatsu','Tama','Miyamae','Asao']

#for names in ward_name_list:
#    combine_pop_loc(city_name,names)

def read_name_list(pref_name):
    with open(f'lists/{pref_name}.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    pref_nl = data['pref']
    city_nl = data['city']
    read_num = data['num']

    return pref_nl, city_nl, read_num


def get_loc_overpy(pref_name, city_name):
    api = overpy.Overpass()
    if 'add' in city_name:
        query = f"""
            [out:json];
            (area[name="{pref_name['jp']}"];)->.a;
            (node(area.a)[place~"^(neighbourhood|quarter)$"];)->.aa;
            (area[name="{city_name['add']}"];)->.b;
            (node(area.b)[place~"^(neighbourhood|quarter)$"];)->.bb;
            (area[name="{city_name['jp']}"];)->.c;
            (node(area.b)[place~"^(neighbourhood|quarter)$"];)->.cc;
            node.aa.bb.cc;
            out;
            """
    else:
        query = f"""
            [out:json];
            (area[name="{pref_name['jp']}"];)->.a;
            (node(area.a)[place~"^(neighbourhood|quarter)$"];)->.aa;
            (area[name="{city_name['jp']}"];)->.b;
            (node(area.b)[place~"^(neighbourhood|quarter)$"];)->.bb;
            node.aa.bb;
            out;
            """

    result = api.query(query)
    data = []
    for node in result.nodes:
        name = node.tags.get("official_name", node.tags.get("name", ""))
        name = zenkaku_replace(name)
        data.append([node.lon, node.lat, name])
    to_write_col = ['lon', 'lat', 'name']
    file_path = f"data/{pref_name['en']}/{pref_name['en']}_{city_name['en']}_loc.tsv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #write_to_tsv(f"data/{pref_name['en']}/{pref_name['en']}_{city_name['en']}_loc.tsv", to_write_col, data)
    with open(file_path, "w", encoding='utf-8') as file:
        # 写入头部
        file.write("\t".join(to_write_col) + "\n")
        # 写入数据
        for row in data:
            file.write("\t".join(map(str, row)) + "\n")


def get_pop_from_excel(pref_name, city_name, path, is_seireishi=False):
    df = pd.read_excel(f'xls/{path}.xlsx', sheet_name=f'{path}')

    # 假设你要筛选的列名为 'ColumnA'，特定元素为 'Value'
    filter_column_index = 3
    if is_seireishi:
        filter_value = f"{pref_name['jp']}{city_name['jp']}"
    elif 'add' in city_name:
        filter_value = f"{city_name['add']}{city_name['jp']}"
    else:
        filter_value = city_name['jp']
    filtered_df = df[df.iloc[:, filter_column_index] == filter_value]

    # 提取筛选行中的特定列，假设这些列是第1列和第2列（ColumnB 和 ColumnC）
    selected_column_indices = [4, 6]
    result_df = filtered_df.iloc[:, selected_column_indices]
    # 打印结果
    result_df.to_csv(f'data/{pref_name["en"]}/{pref_name["en"]}_{city_name["en"]}_pop.tsv',
                     sep='\t', index=False, header=False)


def write_mod_txt(pref_name, city_name, path):
    file_path = path
    with open(file_path, 'a',encoding='utf-8') as file:
        file.write(f"\n[POILayer]\n")
        file.write(f"id=KM_{pref_name['en']}_{city_name['en']}\n")
        if "add" in city_name:
            file.write(f"name={pref_name['jp']}——{city_name['add']}——{city_name['jp']}\n")
        else:
            file.write(f"name={pref_name['jp']}——{city_name['jp']}\n")
        file.write(f"tsv=KM_{pref_name['en']}_{city_name['en']}.tsv\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter the name of the list using --name')
    parser.add_argument('--name',type=str,help='name of the list')
    parser.add_argument('--is_seireishi',action='store_true')
    parser.add_argument('--gappei',action='store_true')
    args = parser.parse_args()
    if not args.name:
        args.name = input(print('Please enter the list name to generate:'))

    prefecture_name = args.name
    seireishi = args.is_seireishi
    pref_name_dict, city_name_list, file_num = read_name_list(prefecture_name)
    xlsx_path = f'b2_032-1_{file_num}'
    mod_path = f"mod/KM_POI_{pref_name_dict['en']}/mod.txt"
    desc = f'Hiring Data POI of {prefecture_name}'
    os.makedirs(os.path.dirname(mod_path), exist_ok=True)
    with open(mod_path, 'w') as f:
        f.write(f"[ModMeta]\nschema=1\nname={desc}\nauthor=KaraageMajo\ndesc={desc}\nversion=1.0.0\n")
    for city_name_dict in city_name_list:
        get_loc_overpy(pref_name_dict, city_name_dict)
        get_pop_from_excel(pref_name_dict, city_name_dict, xlsx_path, seireishi)
        combine_pop_loc(pref_name_dict, city_name_dict)
        write_mod_txt(pref_name_dict, city_name_dict, mod_path)
        print(f"{city_name_dict['jp']} {city_name_dict['en']} done")

    if args.gappei:
        print('start generating simpler mod')
        gappei.gappei(prefecture_name)

    print("Mod generation finished!")
