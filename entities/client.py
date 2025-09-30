from backend.supermarket import Supermarket
from psycopg2 import sql
supermarket = Supermarket()

def close_connection():
    supermarket.end_connection()
    print("\n--> Connection closed.")