import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_5"
response = requests.get(url)

if response.status_code == 200:
    # Parseia o HTML com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra a tabela desejada
    table = soup.find('table', {'id': 'softwarelist'})

    # Extrai os cabeçalhos e as linhas da tabela
    headers = [th.text.strip() for th in table.find('tr').find_all('th') if not th.has_attr('colspan')][:-2]
    regions = [th.text.strip() for th in table.find_all('tr')[1].find_all('th')]

    for row in regions:
        headers.append(row)

    rows = []
    for row in table.find_all('tr')[2:]:
        row_values = [td.text.strip() or '-' for td in row.find_all(['th', 'td'])[:-2]]
        rows.append(row_values)

    # Converte os dados em um DataFrame do pandas
    df = pd.DataFrame(rows, columns=headers)

    # Faz a checagem e limpeza dos dados
    df.dropna(inplace=True)  # Remove linhas com valores nulos
    df.drop_duplicates(inplace=True)  # Remove linhas duplicadas

    # Exporta o DataFrame para um arquivo CSV
    df.to_csv('./Mini Projeto 1/PlayStation5/jogos.csv', index=False)

else:
    print("Erro ao fazer a requisição:", response.status_code)