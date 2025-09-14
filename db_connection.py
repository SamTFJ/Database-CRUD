# dbconnection.py
import os
import psycopg2
from psycopg2 import sql, OperationalError, DatabaseError
from dotenv import load_dotenv
from typing import Any, List, Optional

# Garante que as variáveis de ambiente sejam carregadas do arquivo .env da pasta atual
# O `override=True` faz com que as variáveis do .env substituam as que já existirem no sistema
load_dotenv(dotenv_path=".env", override=True)

class DBconnect:
    """
    Classe responsável por gerenciar a conexão com o banco de dados PostgreSQL,
    abstraindo as operações de conexão, execução de comandos e encerramento.
    """
    def __init__(self):
        # Atributo que armazenará o objeto da conexão
        self.conn: Optional[psycopg2.extensions.connection] = None
        # Atributo que armazenará o cursor para executar comandos SQL
        self.cur: Optional[psycopg2.extensions.cursor] = None
        # Inicia a conexão assim que um objeto DBconnect é criado
        self._connect()

    def _connect(self):
        """
        Método privado que estabelece a conexão com o banco de dados usando as
        credenciais carregadas do arquivo .env.
        """
        try:
            # Tenta conectar ao banco de dados PostgreSQL
            self.conn = psycopg2.connect(
                dbname=os.getenv("db_name"),
                user=os.getenv("db_user"),
                password=os.getenv("db_password"),
                host=os.getenv("db_host"),
                port=os.getenv("db_port")
            )
            # Cria um cursor, que é usado para executar as queries
            self.cur = self.conn.cursor()
        except (OperationalError, Exception) as err:
            # Em caso de erro na conexão, imprime a falha e redefine os atributos para None
            print("\nErro ao conectar com o PostgreSQL:", err)
            self.conn = None
            self.cur = None

    def end_connection(self):
        """
        Fecha o cursor e a conexão com o banco de dados de forma segura.
        """
        try:
            # Garante que o cursor e a conexão sejam fechados se estiverem abertos
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print("\nErro ao fechar a conexão:", e)
        finally:
            # O bloco 'finally' garante que os atributos serão resetados para None,
            # independentemente de ter ocorrido um erro ou não.
            self.cur = None
            self.conn = None

    def _ensure_connection(self):
        """
        Verifica se a conexão está ativa. Se não estiver, tenta reconectar.
        Levanta um erro se a conexão não puder ser estabelecida.
        """
        # Se a conexão ou o cursor não existirem, chama o método _connect para tentar reconectar
        if self.conn is None or self.cur is None:
            self._connect()
        # Se, mesmo após a tentativa, a conexão ainda for nula, lança uma exceção
        if self.conn is None or self.cur is None:
            raise ConnectionError("\nNenhuma conexão com o banco de dados disponível.")

    def execute_command(self, sqlcommand: Any, params: Optional[tuple] = None,
                          fetch: bool = False, fetch_one: bool = False) -> Optional[List[tuple]]:
        """
        Executa um comando SQL de forma segura.

        - sqlcommand: String SQL ou objeto psycopg2.sql.SQL.
        - params: Tupla com parâmetros para a consulta (importante para evitar SQL Injection).
        - fetch: Se True, retorna todos os resultados da consulta (`fetchall`).
        - fetch_one: Se True, retorna apenas o primeiro resultado da consulta (`fetchone`).
        - Lança uma exceção em caso de erro na execução.
        """
        try:
            # Garante que há uma conexão ativa antes de executar qualquer comando
            self._ensure_connection()
            # Executa o comando SQL passando os parâmetros de forma segura
            self.cur.execute(sqlcommand, params)
            
            # Tenta realizar o commit para salvar as alterações (INSERT/UPDATE/DELETE).
            # É seguro chamar sempre, pois não afeta comandos de leitura (SELECT).
            try:
                self.conn.commit()
            except Exception:
                # Em algumas transações de apenas leitura, o commit não é necessário; a exceção é ignorada.
                pass

            # Se a flag fetch_one for True, busca e retorna apenas uma linha de resultado
            if fetch_one:
                return [self.cur.fetchone()]
            # Se a flag fetch for True, busca e retorna todas as linhas de resultado
            if fetch:
                return self.cur.fetchall()
            
            # Se não for uma consulta de busca, retorna None
            return None
        except (DatabaseError, Exception) as e:
            # Em caso de erro durante a execução, desfaz a transação (rollback).
            # Isso garante que o banco de dados não fique em um estado inconsistente.
            if self.conn:
                try:
                    self.conn.rollback()
                except Exception:
                    pass
            print("\nErro no banco de dados:", e)
            # Re-lança a exceção para que a função que chamou este método saiba do erro
            # e possa tratá-lo adequadamente.
            raise