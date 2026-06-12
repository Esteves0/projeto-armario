from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from psycopg2.extras import RealDictCursor
from database import get_connection

app = Flask(__name__)
app.secret_key = "chave_secreta_senai_lockers"


# Rota raiz (redireciona automaticamente para o login)
@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/filtrar_armarios', methods=['GET'])
def filtrar_armarios():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        filtro_aplicado = request.args.get('filtro_status')
        if filtro_aplicado == 'ocupados':
            sql = "SELECT * FROM armarios WHERE status = %s ORDER BY numero ASC"
            cur.execute(sql, (True,))
            armarios_ocupados = cur.fetchall()
            return render_template('index.html', armarios=armarios_ocupados, filtro_ativo=filtro_aplicado)
        elif filtro_aplicado == 'desocupados':
            sql = "SELECT * FROM armarios WHERE status = %s ORDER BY numero ASC"
            cur.execute(sql, (False,))
            armarios_desocupados = cur.fetchall()
            return render_template('index.html', armarios=armarios_desocupados,filtro_ativo=filtro_aplicado)
        else:
            sql = "SELECT * FROM armarios ORDER BY numero ASC"
            cur.execute(sql)
            todos_armarios = cur.fetchall()
            return render_template('index.html', armarios=todos_armarios, filtro_ativo=filtro_aplicado )
    except Exception as e:
        return f"Ocorreu um erro: {e}"
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()


@app.route('/armarios')
def armarios():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        sql = 'SELECT * FROM armarios ORDER BY numero ASC'
        cur.execute(sql)
        dados_armarios = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", armarios=dados_armarios)
    except Exception as e:
        return jsonify({"message": f"Erro ao listar armários: {e}"}), 500


@app.route('/buscar_armario', methods=['GET'])
def buscar_armario():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        id_busca = request.args.get('numero_armario')

        sql = 'SELECT * FROM armarios WHERE numero = %s'
        cur.execute(sql, (id_busca,))
        armario_buscado = cur.fetchone()

        if armario_buscado:
            cur.close()
            conn.close()
            return render_template("index.html", armarios=[armario_buscado])

        else:
            flash(f"O armário n° {id_busca} não existe no sistema.", "erro")

            cur.execute('SELECT * FROM armarios ORDER BY numero ASC')
            todos_armarios = cur.fetchall()

            cur.close()
            conn.close()

            return render_template("index.html", armarios=todos_armarios)

    except Exception as e:
        if 'cur' in locals() and not cur.closed: cur.close()
        if 'conn' in locals(): conn.close()
        return f"Ocorreu um erro na busca: {e}"





# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # Só abre a conexão com o banco se for um envio de formulário (POST)
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            cur.execute('SELECT * FROM "adm_login" WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                if user['senha'] == password:
                    # LOGIN SUCESSO: Redireciona mudando a URL lá em cima
                    return redirect(url_for('armarios'))
                else:
                    return "Senha incorreta"
            else:
                return "Email não registrado"
        except Exception as e:
            return f"Ocorreu um erro: {e}"
        finally:
            # Garante que o banco fecha independentemente de dar erro ou sucesso
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()


# Rota de Cadastro
@app.route('/cadastro_user', methods=['GET', 'POST'])
def cadastrar_user():
    if request.method == 'GET':
        return render_template('cadastro_user.html')

    if request.method == 'POST':
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            sql1 = 'SELECT * FROM adm_login WHERE email = %s'
            sql2 = 'INSERT INTO adm_login(nome, email, senha) VALUES (%s, %s, %s)'
            params = (name, email, password)

            cur.execute(sql1, (email,))
            user = cur.fetchone()
            if user:
                return "Email já cadastrado"
            else:
                cur.execute(sql2, params)
                conn.commit()
                return redirect(url_for("armarios"))
        except Exception as e:
            return f"Ocorreu um erro: {e}"
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()


@app.route('/ficha_armario/<int:id>')
def ficha_armario(id):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # 1. Busca os dados do armário pelo número
        sql = 'SELECT * FROM armarios WHERE numero = %s'
        cur.execute(sql, (id,))
        d_armario = cur.fetchone()

        d_aluno = None

        # 2. Correção: Verifica se o armário existe e possui um 'aluno_id' vinculado
        if d_armario and d_armario.get('aluno_id'):
            sql_aluno = "SELECT * FROM alunos WHERE id = %s"
            cur.execute(sql_aluno, (d_armario['aluno_id'],))
            d_aluno = cur.fetchone()

        cur.close()
        conn.close()

        return render_template("ficha_armario.html", armario=d_armario, aluno=d_aluno)
    except Exception as e:
        return f"Ocorreu um erro: {e}"


@app.route('/ficha_armario/editar/<int:id>', methods=['GET', 'POST'])
def editar_armario(id):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == 'GET':
            cur.execute('SELECT * FROM armarios WHERE numero = %s', (id,))
            d_armario = cur.fetchone()

            cur.execute('SELECT id, nome FROM alunos ORDER BY nome ASC')
            lista_alunos = cur.fetchall()

            cur.close()
            conn.close()
            return render_template("editar_ficha.html", armario=d_armario, alunos=lista_alunos)

        if request.method == 'POST':
            status_novo = request.form.get('status') == '1'
            id_aluno_novo = request.form.get('id_aluno')  # Mantém o que vem do formulário

            # VALIDAÇÃO: Se tiver aluno selecionado, impede de salvar como "Desocupado"
            if id_aluno_novo != "" and not status_novo:
                return "Erro: Não é possível definir o armário como 'Desocupado' se ele possui um aluno vinculado. Remova o aluno ou altere o status para 'Ocupado'."

            if not status_novo or id_aluno_novo == "":
                id_aluno_novo = None

            # CORREÇÃO AQUI: Mudado de id_aluno para aluno_id para bater com o seu banco de dados
            sql_update = 'UPDATE armarios SET status = %s, aluno_id = %s WHERE numero = %s'
            cur.execute(sql_update, (status_novo, id_aluno_novo, id))
            conn.commit()

            cur.close()
            conn.close()
            return redirect(url_for('ficha_armario', id=id))

    except Exception as e:
        return f"Ocorreu um erro ao editar: {e}"
    finally:
        if 'cur' in locals() and not cur.closed: cur.close()
        if 'conn' in locals(): conn.close()

@app.route('/cadastro_aluno', methods=['GET', 'POST'])
def cadastrar_aluno():

    try:

        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if request.method == 'GET':
            return render_template('cadastrar_aluno.html')


        if request.method == 'POST':
            nome = request.form.get('nome')
            cpf = request.form.get('cpf')
            turma = request.form.get('turma')
            contato = request.form.get('contato')
            sql_busca = 'SELECT * FROM alunos WHERE cpf = %s AND nome = %s'

            cur.execute(sql_busca, (cpf, nome))
            aluno = cur.fetchone()
            if aluno:
                return "Aluno já cadastrado"
            else:
                sql = 'INSERT INTO alunos (nome, cpf,contato, turma) VALUES(%s,%s,%s,%s)'
                cur.execute(sql, (nome, cpf, contato, turma))
                conn.commit()
                return redirect(url_for("armarios"))

    except Exception as e:
        return f"Ocorreu um erro: {e}"
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()


if __name__ == '__main__':
    app.run(debug=True)