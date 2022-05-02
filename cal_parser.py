# -*- coding: utf-8 -*-
"""
Created on Sun May  1 22:45:11 2022

@author: Leon G
"""
import pandas as pd
from datetime import datetime


path_excel_cal_file = "example_cal.xls"
path_output_cal_file = "output_cal.xlsx"
month = 4
card_field="1212"
final_excel_column_list = ['date',
    'company',
    'category',
    'card',
    'deal_type',
    'charge_sum',
    'charge_coin',
    'total_sum',
    'total_sum_coin',
    'charge_date',
    'additinal_info'
    ]

def open_xls_file_in_cal_format(filename):
    with open(filename, encoding = "utf-16") as file:
        lines_from_xls = file.readlines()
    lines_new = []
    for line in lines_from_xls:
        lines_new.append(line.split('\t'))
    return pd.DataFrame(lines_new)

def clean_df_received_from_excel(filename):
    df_result = open_xls_file_in_cal_format(path_excel_cal_file)
    df_result.columns = df_result.iloc[2]
    df_result = df_result[3:-1]
    df_result['תאריך העסקה'] = pd.to_datetime(df_result['תאריך העסקה'], format="%d/%m/%y")
    return df_result

def split_total_deal_column(df):
    return df['total_sum_charged'].str.split(' ', n=-1, expand=True)

def split_current_charge_sum_column(df):
    return df['amount_charged_current_time'].str.split(' ', n=-1, expand=True)


def extract_charge_amounts(df):
    df[['total_sum_coin', 'total_sum']] = split_total_deal_column(df)#df['סכום העסקה'].str.split(' ', n=-1, expand=True)
    df[['charge_coin', 'charge_sum']] = split_current_charge_sum_column(df)#df['סכום העסקה'].str.split(' ', n=-1, expand=True)
    df['total_sum'] = df['total_sum'].str.replace(',', '').astype('float')
    df['charge_sum'] = df['charge_sum'].str.replace(',', '').astype('float')
    return df.drop(['total_sum_charged', 'amount_charged_current_time'], axis=1)

def transform_columns(df):
    df.columns = ['date', 'company', 'total_sum_charged', 'amount_charged_current_time', 'additinal_info']
    df = extract_charge_amounts(df)
    df.insert(2,"category", value="", allow_duplicates=True)
    df.insert(3,"card", value=card_field, allow_duplicates=True)
    df.insert(4,"deal_type", value="", allow_duplicates=True)
    df.insert(9,"charge_date", value="", allow_duplicates=True)
    df = df.reindex(columns=final_excel_column_list)
    return df

df = clean_df_received_from_excel(path_excel_cal_file)
df = transform_columns(df)


df.to_excel(path_output_cal_file)