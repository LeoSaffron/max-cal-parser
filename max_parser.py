# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 22:13:05 2022

@author: Leon G
"""

import pandas as pd


path_excel_input_list = [
    "example1.xlsx",
    "example2.xlsx",
    "example3.xlsx"
    ]
path_excel_max_file = "example-input.xlsx"
path_output_excel_file = "max.xlsx"
month = 4

xls = pd.ExcelFile(path_excel_max_file)


def parse_sheet_by_index(xls, sheet_index, month_to_filter=0):
    sheet_to_parse = pd.read_excel(xls, sheet_name=xls.sheet_names[sheet_index])
    sheet_to_parse = sheet_to_parse[2:]
    sheet_to_parse.columns = sheet_to_parse.iloc[0]
    sheet_to_parse = sheet_to_parse.T[:11].T
    sheet_to_parse = sheet_to_parse[1:]
    sheet_to_parse['תאריך עסקה'] = pd.to_datetime(sheet_to_parse['תאריך עסקה'], format="%d-%m-%Y")
    if month_to_filter > 0:
        sheet_to_parse = sheet_to_parse[sheet_to_parse['תאריך עסקה'].dt.month == month_to_filter]
    return sheet_to_parse


# max_this_month = parse_sheet_by_index(0, month_to_filter=4)
# max_not_yet_approved = parse_sheet_by_index(1, month_to_filter=4)
# max_foreign_this_month = parse_sheet_by_index(2, month_to_filter=4)
# max_foreign_general = parse_sheet_by_index(3, month_to_filter=4)


def parse_whole_excel(path_filename, month_to_filter):
    xls_result = pd.ExcelFile(path_filename)
    df_result = pd.DataFrame()
    for i in range(len(xls.sheet_names)):
        df_result = pd.concat([df_result, parse_sheet_by_index(xls_result, i, month_to_filter=month)])
    return df_result

def read_excel_list_info_single_df(path_list):
    dflist = []
    for filename in path_list:
        # df_result = parse_whole_excel(filename, month)
        # dflist.append(df_result)
        dflist.append(parse_whole_excel(filename, month))
        
    df_result = pd.concat(dflist)
    df_result.sort_values(by='תאריך עסקה')
    return df_result
# result_df = parse_whole_excel(path_excel_max_file, month)
result_df = read_excel_list_info_single_df(path_excel_input_list)
display(result_df)


result_df.to_excel(path_output_excel_file)