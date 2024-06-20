import pandas as pd
import json
import csv
from openpyxl import load_workbook
from datetime import datetime
import re

def ler_arquivos():
    try:
        csv_df = pd.read_csv('./Mini Projeto 2/usuarios_csv.csv')

        with open('./Mini Projeto 2/usuarios_json.json') as f:
            json_data = json.load(f)
        json_df = pd.DataFrame(json_data)

        excel_df = pd.read_excel('./Mini Projeto 2/usuarios_excel.xlsx')

        return csv_df, json_df, excel_df

    except FileNotFoundError as e:
        print(f"Erro ao ler arquivo: {e}")
        return None, None, None
    
def limpar_dados(df):

    df.drop_duplicates(inplace=True)
    df.fillna('', inplace=True)

    # Filtrar emails válidos
    df = df[df['email'].apply(lambda x: re.match(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', x) is not None)]

    # Filtrar datas no formato YYYY-MM-DD
    df = df[df['data_nascimento'].apply(lambda x: isinstance(x, str) and re.match(r'\d{4}-\d{2}-\d{2}', x) is not None)]

    return df

def consolidar_dados(csv_df, json_df, excel_df):
    try:
        df = pd.concat([csv_df, json_df, excel_df], ignore_index=True)

        # Remover duplicatas novamente
        df.drop('id', axis=1, inplace=True)
        df.drop_duplicates(inplace=True)

        return df

    except Exception as e:
        print(f"Erro ao concatenar DataFrames: {e}")
        return None
    

def exportar_para_excel(df):
    try:
        df.to_excel('./Mini Projeto 2/usuarios_consolidados.xlsx', index=False)

        print("Arquivo exportado com sucesso!")

    except Exception as e:
        print(f"Erro ao exportar para Excel: {e}")


if __name__ == '__main__':
    csv_df, json_df, excel_df = ler_arquivos()

    if csv_df is not None and json_df is not None and excel_df is not None:
        csv_df = limpar_dados(csv_df)
        json_df = limpar_dados(json_df)
        excel_df = limpar_dados(excel_df)

        df = consolidar_dados(csv_df, json_df, excel_df)

        if df is not None:
            exportar_para_excel(df)