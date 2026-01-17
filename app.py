from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configs iniciais ---
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG") == "True"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

DATABASE = "biblioteca.db"


def get_db_connection():
    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Classe do usuário para Flask-Login ---
class Usuario(UserMixin):
    def __init__(self, id, usuario, senha):
        self.id = id
        self.usuario = usuario
        self.senha = senha

# --- Função para pegar usuário do banco ---
def get_usuario_por_nome(usuario):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    user = c.fetchone()
    conn.close()

    if user:
        return Usuario(id=user["id"], usuario=user["usuario"], senha=user["senha"])
    return None

def get_usuario_por_id(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    user = c.fetchone()
    conn.close()
    if user:
        return Usuario(id=user[0], usuario=user[1], senha=user[2])
    return None

@login_manager.user_loader
def load_user(user_id):
    return get_usuario_por_id(user_id)


# --- Rotas ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        usuario = request.form['usuario']
        senha = request.form['senha']

        user = get_usuario_por_nome(usuario)
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Usuário ou senha incorretos!", "error")
            return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da conta.", "info")
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Checa se usuário já existe
        if get_usuario_por_nome(usuario):
            flash("Esse usuário já existe!", "error")
            return redirect(url_for('register'))

        # Hash da senha
        senha_hash = generate_password_hash(senha)

        # Salva no banco
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_hash))
        conn.commit()
        conn.close()

        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    livros = conn.execute('SELECT * FROM livros').fetchall()
    conn.close()
    return render_template(
        'home.html',
        usuario=current_user.usuario,
        livros=livros
    )


@app.route('/cadastrar')
def cadastrar_form():
    return render_template('cadastrar.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano = request.form['ano']
    estado = request.form['estado']

    conn = get_db_connection()
    conn.execute('INSERT INTO livros (nome, autor, ano, estado) VALUES (?, ?, ?, ?)', (titulo, autor, ano, estado))
    conn.commit()
    conn.close()

    return redirect('/')


# --- Rodar app ---
if __name__ == "__main__":
    app.run(debug=debug_mode)
