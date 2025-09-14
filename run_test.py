import os
import psycopg2
from dotenv import load_dotenv

# garante que carrega do .env da pasta atual
load_dotenv(dotenv_path=".env")

print("Variáveis carregadas:")
print("DB:", os.getenv("db_name"))
print("USER:", os.getenv("db_user"))
print("HOST:", os.getenv("db_host"))

conn = psycopg2.connect(
    dbname=os.getenv("db_name"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    host=os.getenv("db_host"),
    port=os.getenv("db_port")
)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM item;")
print("Itens cadastrados:", cur.fetchone()[0])
cur.close()
conn.close()
