from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

# Criar engine do banco de dados
engine = create_engine(f'sqlite:///Projeto Integrador/banco_de_jogos.db')

# Criar base de dados
Base = declarative_base()

class Consoles(Base):
    __tablename__ = 'consoles'
    id = Column(Integer, primary_key=True)
    console = Column(String)

class UsuarioConsole(Base):
    __tablename__ = 'usuario_console'
    id = Column(Integer, primary_key=True)
    usuario = Column(Integer, ForeignKey('usuarios.id'))
    idConsole = Column(Integer, ForeignKey('consoles.id'))

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    data_nascimento = Column(String)
    email = Column(String)
    cidade = Column(String)

class JogosMercadoLivre(Base):
    __tablename__ = 'jogos_mercado_livre'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Float)
    permalink = Column(String)

class JogosPreferidos(Base):
    __tablename__ = 'jogos_preferidos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

# Criar tabelas no banco de dados
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()