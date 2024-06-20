import requests
import pandas as pd
import sqlalchemy as db
import sqlite3
from time import sleep

# Conectar ao banco de dados
engine = db.create_engine(f'sqlite:///Mini Projeto 4/jogos_mercado.db')
conn = sqlite3.connect(f'./Mini Projeto 3/jogos.db')
cursor = conn.cursor()

# Ler a lista de jogos únicos do banco de dados
cursor.execute('SELECT Jogo FROM jogos_unicos')
jogos_unicos = [row[0] for row in cursor.fetchall()]

# Criar um DataFrame para armazenar os dados
df = pd.DataFrame(columns=['nome', 'preco', 'permalink'])

# Consultar a API do Mercado Livre para cada jogo
for jogo in jogos_unicos:
    try:
        # Montar a URL da rota da API
        url = f'https://api.mercadolibre.com/sites/MLB/search?category=MLB186456&q={jogo.replace(" ", "%20")}'

        # Realizar a consulta à API
        response = requests.get(url)
        response.raise_for_status()

        # Extrair nome, preço e permalink dos resultados
        results = response.json()['results']
        for result in results:
            nome = result['title']
            preco = result['price']
            permalink = result['permalink']
            df.loc[len(df)] = [nome, preco, permalink]

        # Adicionar um atraso para respeitar os limites de taxa da API
        sleep(1)

    except requests.exceptions.RequestException as e:
        print(f'Erro ao consultar a API: {e}')
    except Exception as e:
        print(f'Erro ao processar a resposta: {e}')

# Exportar o DataFrame para o banco de dados
df.to_sql('jogos_mercado_livre', engine, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()