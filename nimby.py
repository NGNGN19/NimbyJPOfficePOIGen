import csv
from pathlib import Path
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


def zenkaku_replace(item:dict):
    item["name"] = item["name"].replace("一丁目","１丁目")
    item["name"] = item["name"].replace("二丁目","２丁目")
    item["name"] = item["name"].replace("三丁目","３丁目")
    item["name"] = item["name"].replace("四丁目","４丁目")
    item["name"] = item["name"].replace("五丁目","５丁目")
    item["name"] = item["name"].replace("六丁目","６丁目")
    item["name"] = item["name"].replace("七丁目","７丁目")
    item["name"] = item["name"].replace("八丁目","８丁目")
    item["name"] = item["name"].replace("九丁目","９丁目")
    item["name"] = item["name"].replace("十丁目","１０丁目")
    item["name"] = item["name"].replace("1丁目","１丁目")
    item["name"] = item["name"].replace("2丁目","２丁目")
    item["name"] = item["name"].replace("3丁目","３丁目")
    item["name"] = item["name"].replace("4丁目","４丁目")
    item["name"] = item["name"].replace("5丁目","５丁目")
    item["name"] = item["name"].replace("6丁目","６丁目")
    item["name"] = item["name"].replace("7丁目","７丁目")
    item["name"] = item["name"].replace("8丁目","８丁目")
    item["name"] = item["name"].replace("9丁目","９丁目")
    item["name"] = item["name"].replace("10丁目","１０丁目")


def combine_pop_loc(name_c, name_w):
        loc_path = f"data/{name_c}/{name_c}_{name_w}_loc.tsv"
        pop_path = f"data/{name_c}/{name_c}_{name_w}_pop.csv"
        loc_col = ["lon", "lat", "name"]
        loc_read = read_from_tsv(loc_path, loc_col)
        # print(loc_read)
        pop_col = ["name", "population"]
        pop_read = read_from_csv(pop_path, pop_col)
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
                zenkaku_replace(loc_item)
                if loc_item["name"] == pop_item['name']:
                    todict = {'lon': 0,
                              'lat': 0,
                              'color': '000000',
                              'text': '',
                              'font_size': 0,
                              'max_lod': 0,
                              'transparent': 1,
                              'demand': "KM_Office",
                              'population': 0}
                    todict['text'] = loc_item['name']
                    todict['lon'] = loc_item['lon']
                    todict['lat'] = loc_item['lat']
                    todict['population'] = pop_item['population']
                    to_write.append(todict)

        to_write_col = ['lon', 'lat', 'color', 'text', 'font_size', 'max_lod', 'transparent', 'demand', 'population']
        write_to_tsv(f"data/{name_c}/KM_{name_c}_{name_w}.tsv", to_write_col, to_write)


city_name = 'Kawasaki'
# ward_name = 'Chiyoda'
# ward_name = input('Input name:')
# ward_name_list = ['Tsurumi','Kanagawa','Nishi','Naka','Minami','Hodogaya','Isogo',
#                   'Kanazawa','Kohoku','Totsuka','Konan','Asahi','Midori','Seya',
#                   'Sakae','Izumi','Aoba','Tsuzuki']
ward_name_list = ['Kawasaki',"Saiwai","Nakahara",'Takatsu','Tama','Miyamae','Asao']

for names in ward_name_list:
    combine_pop_loc(city_name,names)

