import os
import psycopg2
from dotenv import load_dotenv

# Carrega a URL do .env
load_dotenv()


def get_connection():
    db_url = os.getenv('DATABASE_URL')

    if not db_url:
        print("❌ ERRO: A variável DATABASE_URL não foi encontrada. Verifique o .env!")
        return None

    try:
        # O psycopg2 adora quando passamos a URL completa!
        conn = psycopg2.connect(db_url)
        return conn

    except Exception as e:
        print(f"❌ Erro REAL de conexão: {e}")
        return None


if __name__ == "__main__":
    print("Testando a conexão definitiva...")
    conn = get_connection()
    if conn:
        print("✅ SUCESSO ABSOLUTO! O Neon abriu as portas!")
        conn.close()
    else:
        print("❌ Ainda não deu. Veja o erro acima.")