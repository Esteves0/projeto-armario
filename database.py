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


def inicializar_banco():
    """Função para criar as tabelas e gerar os armários se eles não existirem"""
    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()


        
        total_armarios = 100
        print(f"Verificando/Criando {total_armarios} armários no Neon...")
        
        for numero in range(1, total_armarios + 1):
            cursor.execute("""
                INSERT INTO armarios (numero, status) 
                VALUES (%s, FALSE)
                ON CONFLICT (numero) DO NOTHING;
            """, (numero,))

        # Salva tudo no Neon
        conn.commit()
        print("✅ Banco de dados inicializado e armários gerados com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao inicializar o banco: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Testando a conexão definitiva...")
    conn = get_connection()
    if conn:
        print("✅ SUCESSO ABSOLUTO! O Neon abriu as portas!")
        conn.close()
        
        # Pergunta se deseja resetar/inicializar os armários
        resposta = input("Deseja rodar a inicialização dos armários agora? (s/n): ")
        if resposta.lower() == 's':
            inicializar_banco()
    else:
        print("❌ Ainda não deu. Veja o erro acima.")

