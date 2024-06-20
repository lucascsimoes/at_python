import pandas as pd
import sqlalchemy as db
import collections

path = './Mini Projeto 3/'
engine = db.create_engine(f'sqlite:///{path}/jogos.db')

try:
    df = pd.read_excel('./Mini Projeto 2/usuarios_consolidados.xlsx')
except Exception as e:
    print(f'Erro ao ler o arquivo Excel: {e}')
    exit()


def get_jogos_unicos(df):
    jogos = set()
    for row in df['jogos_preferidos']:
        jogos.update(row.split('|'))
    return jogos



def get_jogos_mais_citados(df):
    jogos = set()
    for row in df['jogos_preferidos']:
        jogos.update(row.split('|'))
    
    contador_jogos = collections.Counter()
    for row in df['jogos_preferidos']:
        contador_jogos.update(row.split('|'))
    
    jogos_mais_citados = contador_jogos.most_common(3)
    return jogos_mais_citados


def get_jogos_citados_uma_vez(df):
    jogos = set()
    for row in df['jogos_preferidos']:
        jogos.update(row.split('|'))
    
    contador_jogos = collections.Counter()
    for row in df['jogos_preferidos']:
        contador_jogos.update(row.split('|'))

    jogos_uma_vez = [jogo for jogo, contagem in contador_jogos.items() if contagem == 1]

    return jogos_uma_vez


jogos_unicos = get_jogos_unicos(df)
jogos_mais_citados = get_jogos_mais_citados(df)
jogos_citados_uma_vez = get_jogos_citados_uma_vez(df)


# Exportando sets para SQLite
try:
    pd.DataFrame(list(jogos_unicos), columns=['Jogo']).to_sql('jogos_unicos', engine, if_exists='replace', index=False)
    pd.DataFrame(list(jogos_mais_citados), columns=['Jogo', 'Quantidade']).to_sql('jogos_mais_citados', engine, if_exists='replace', index=False)
    pd.DataFrame(list(jogos_citados_uma_vez), columns=['Jogo']).to_sql('jogos_citados_uma_vez', engine, if_exists='replace', index=False)
except Exception as e:
    print(f"Erro ao exportar dados para o banco de dados: {e}")