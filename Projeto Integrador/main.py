import pandas as pd
import sqlalchemy as db
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from tabelas import engine, session, Consoles, UsuarioConsole, Usuarios, JogosMercadoLivre, JogosPreferidos
import sqlite3


usuarios_consolidados = pd.read_excel('./Mini Projeto 2/usuarios_consolidados.xlsx')
usuarios_consolidados.fillna('Nenhum', inplace=True)

# Inserindo consoles
if session.query(Consoles).count() == 0:
    consoles = set()
    for row in usuarios_consolidados['consoles']:
        consoles.update(row.split('|'))

    for index, console in enumerate(consoles):
        session.add(Consoles(
            id = index + 1,
            console = console
        ))

    session.commit()



# Inserindo usuarios com console
if session.query(UsuarioConsole).count() == 0:
    query = session.query(Consoles.id, Consoles.console).all()
    usuario_console_df = usuarios_consolidados[['nome_completo', 'consoles']]
    usuario_console_df.loc[:, 'consoles'] = usuario_console_df['consoles'].str.split('|')
    usuario_console_df = usuario_console_df.explode('consoles')
    usuario_console_df.reset_index(drop=True, inplace=True)

    console_dict = dict((y, x) for x, y in query)
    usuario_console_df['consoles'] = usuario_console_df['consoles'].map(console_dict)

    for usuario in usuario_console_df.iterrows():
        session.add(UsuarioConsole(
            id = usuario[0] + 1,
            usuario = usuario[1][0],
            idConsole = usuario[1][1]
        ))

    session.commit()



# Inserindo usuarios
if session.query(Usuarios).count() == 0:
    for index, usuario in enumerate(usuarios_consolidados[['nome_completo', 'data_nascimento', 'email', 'cidade']].values.tolist()):
        session.add(Usuarios(
            id = index + 1,
            nome = usuario[0],
            data_nascimento = usuario[1],
            email = usuario[2],
            cidade = usuario[3]
        ))

    session.commit()


# Inserindo Jogos Mercado Livre
if session.query(JogosMercadoLivre).count() == 0:
    conn = sqlite3.connect(f'./Mini Projeto 4/jogos_mercado.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM jogos_mercado_livre')
    for index, jogo in enumerate(cursor.fetchall()):
        session.add(JogosMercadoLivre(
            id = index + 1,
            nome = jogo[0],
            preco = jogo[1],
            permalink = jogo[2]
        ))
            
    session.commit()



# Inserindo Jogos Preferidos
if session.query(JogosPreferidos).count() == 0:
    conn = sqlite3.connect(f'./Mini Projeto 3/jogos.db')
    cursor = conn.cursor()

    cursor.execute('SELECT Jogo FROM jogos_mais_citados')
    for index, jogo in enumerate(cursor.fetchall()):
        print()
        session.add(JogosPreferidos(
            id = index + 1,
            nome = jogo[0]
        ))
            
    session.commit()

