import csv
import json
import overpy
import pandas as pd
import os
import argparse
from zenkaku_replace import zenkaku_replace, simpler_zenkaku_replace
import gappei
import nimby


def get_loc_kokkou(pref_name,city_name,encoding='Shift-JIS'):
    loc_path = f'loc/{pref_name["num"]}_{pref_name["year"]}.csv'
    kokkou_col=["都道府県コード","都道府県名","市区町村コード","市区町村名","大字町丁目コード","大字町丁目名","緯度","経度","原典資料コード","大字・字・丁目区分コード"]
    col_to_keep = ["大字町丁目名","緯度","経度"]
    loc_list=nimby.read_from_csv(loc_path,kokkou_col,encoding=encoding)
    if 'add' in city_name:
        filter_value = f"{city_name['add']}{city_name['jp']}"
    elif 'seireishi' in pref_name:
        filter_value = f"{pref_name['jp']}{city_name['jp']}"
    else:
        filter_value = city_name['jp']
    filtered_list=[{key : value for key, value in item.items() if key in col_to_keep }
                   for item in loc_list 
                   if item['市区町村名']==filter_value
    ]
    do_jo_conv = city_name.get('jo_conv',False)
    do_cho_conv = city_name.get('cho_conv',False)
    for item in filtered_list:
        item["大字町丁目名"] = simpler_zenkaku_replace(item["大字町丁目名"],do_jo_conv=do_jo_conv,do_cho_conv=do_cho_conv)

    output_path = f"data/{pref_name['en']}/{pref_name['en']}_{city_name['en']}_loc.tsv"
    to_write_col = ["経度","緯度","大字町丁目名"]
    nimby.write_to_tsv(output_path,to_write_col,filtered_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter the name of the list using --name')
    parser.add_argument('--name',type=str,help='name of the list',required=True)
    parser.add_argument('--is_seireishi',action='store_true')
    parser.add_argument('--gappei',action='store_true')
    parser.add_argument('--color',type=str,default='ffffff')
    parser.add_argument('--g_color',type=str,default='ff0000')
    parser.add_argument('--encoding',type=str,default='Shift-JIS')
    parser.add_argument('--g_filter',type=int)
    parser.add_argument('--prefix',default='')
    parser.add_argument('--g_prefix',default='Simp_')
    parser.add_argument('--filter',type=int)
    parser.add_argument('--pass_data_collect',action='store_true')
    args = parser.parse_args()
    args_dict = vars(args)

    prefecture_name = args.name
    #seireishi = args.is_seireishi
    nimby.nimby_main(prefecture_name,get_loc_func=get_loc_kokkou,**args_dict)

    if args.gappei:
        print('start generating simpler mod')
        gappei.gappei(prefecture_name,**args_dict)

    print("Mod generation finished!")