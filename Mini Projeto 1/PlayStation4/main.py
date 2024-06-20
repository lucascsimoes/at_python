import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://pt.wikipedia.org/wiki/Lista_de_jogos_para_PlayStation_4"
response = requests.get(url)

if response.status_code == 200:
    # Parseia o HTML com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra a tabela desejada
    table = soup.find('table', {'class': 'wikitable sortable'})

    # Extrai os cabeçalhos e as linhas da tabela
    headers = [th.text.strip() for th in table.find('tr').find_all('th')[:-1]]

    rows = []
    for row in table.find_all('tr')[1:]:
        row_values = [td.text.strip() or '-' for td in row.find_all(['td', 'th'])[:-1]]
        rows.append(row_values)

    # Converte os dados em um DataFrame do pandas
    df = pd.DataFrame(rows, columns=headers)

    # Faz a checagem e limpeza dos dados
    df.dropna(inplace=True)  # Remove linhas com valores nulos
    df.drop_duplicates(inplace=True)  # Remove linhas duplicadas

    # Exporta o DataFrame para um arquivo CSV
    df.to_csv('./Mini Projeto 1/PlayStation4/jogos.csv', index=False)

else:
    print("Erro ao fazer a requisição:", response.status_code)