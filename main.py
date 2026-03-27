from flask import Flask, render_template, request
from psycopg2.extras import RealDictCursor

from database import get_connection


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)


    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')


            cur.execute('SELECT * FROM "adm_login" WHERE email = %s', (email,))
            user = cur.fetchone()
            if user:

                if user['senha'] == password:
                    return render_template('armarios.html')
                else:
                    return "Senha incorreta"
            else:
                return "Email não registrado"
        except Exception as e:
            return f"Ocorreu um erro: {e}"
        finally:
            # No seu bloco login...
            # Sempre feche o cursor antes da conexão
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()






@app.route('/armarios')
def armarios():
    return render_template('armarios.html')

if __name__ == '__main__':
    app.run(debug=True)