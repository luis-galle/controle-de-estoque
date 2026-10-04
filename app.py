from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def criar_banco():
    conexao = sqlite3.connect("estoque.db")

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS produtos
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL
        )
    """)

    conexao.close()

@app.route("/")
def inicio():
    conexao = sqlite3.connect("estoque.db")

    produtos = conexao.execute(
        "SELECT * FROM produtos"
    ).fetchall() 

    conexao.close()
    return render_template("index.html", produtos=produtos)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    quantidade = request.form["quantidade"]
    preco = request.form["preco"]

    conexao = sqlite3.connect("estoque.db")

    conexao.execute(
        "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
        (nome, quantidade, preco)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")

@app.route("/pesquisar")
def pesquisar():
    busca = request.args.get("busca")

    conexao = sqlite3.connect("estoque.db")

    produtos = conexao.execute(
        "SELECT * FROM produtos WHERE nome LIKE ?",
        (f"%{busca}%",)
    ).fetchall()

    conexao.close()

    return render_template("index.html", produtos=produtos, busca=busca)

@app.route("/editar/<int:id>")
def editar(id):
    conexao = sqlite3.connect("estoque.db")

    produto = conexao.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id,)
    ).fetchone()

    conexao.close()

    return render_template("editar.html", produto=produto)

@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    nome = request.form["nome"]
    quantidade = request.form["quantidade"]
    preco = request.form["preco"]

    conexao = sqlite3.connect("estoque.db")

    conexao.execute(
    "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
    (nome, quantidade, preco, id)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")

@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = sqlite3.connect("estoque.db")

    conexao.execute(
    "DELETE FROM produtos WHERE id = ?",
    (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")

criar_banco()

if __name__ == "__main__":
    app.run(debug=True)

