from flask import Flask, render_template

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Rota para a página principal (index)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Rota para a página de armários
@app.route('/armarios')
def armarios():
    return render_template('armarios.html')

# Executa o servidor no modo de depuração (debug)
if __name__ == '__main__':
    app.run(debug=True)