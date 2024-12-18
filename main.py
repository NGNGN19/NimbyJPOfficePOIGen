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
    else:
        filter_value = city_name['jp']
    filtered_list=[{key : value for key, value in item.items() if key in col_to_keep }
                   for item in loc_list 
                   if item['市区町村名']==filter_value
    ]
    do_jo_conv = city_name.get('jo_conv',False)
    for item in filtered_list:
        item["大字町丁目名"] = simpler_zenkaku_replace(item["大字町丁目名"],do_jo_conv)

    output_path = f"data/{pref_name['en']}/{pref_name['en']}_{city_name['en']}_loc.tsv"
    to_write_col = ["経度","緯度","大字町丁目名"]
    nimby.write_to_tsv(output_path,to_write_col,filtered_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter the name of the list using --name')
    parser.add_argument('--name',type=str,help='name of the list')
    parser.add_argument('--is_seireishi',action='store_true')
    parser.add_argument('--gappei',action='store_true')
    parser.add_argument('--color',type=str)
    parser.add_argument('--g_color',type=str)
    parser.add_argument('--encoding',type=str)
    args = parser.parse_args()
    if not args.name:
        args.name = input(print('Please enter the list name to generate:'))
    if not args.color:
        args.color = 'ffffff'
    if not args.g_color:
        args.g_color = 'ff0000'
    if not args.encoding:
        args.encoding = 'Shift-JIS'

    prefecture_name = args.name
    #seireishi = args.is_seireishi
    nimby.nimby_main(prefecture_name,get_loc_func=get_loc_kokkou,color=args.color,is_seireishi=args.is_seireishi)

    if args.gappei:
        print('start generating simpler mod')
        gappei.gappei(prefecture_name,args.g_color)

    print("Mod generation finished!")