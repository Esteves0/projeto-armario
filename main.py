from flask import Flask, render_template, request
from psycopg2.extras import RealDictCursor

from databse import get_connection


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            conn = get_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute('SELECT * FROM "user_adm" WHERE email = %s', (email,))
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
            conn.close()
            cur.close()





@app.route('/armarios')
def armarios():
    return render_template('armarios.html')

if __name__ == '__main__':
    app.run(debug=True)