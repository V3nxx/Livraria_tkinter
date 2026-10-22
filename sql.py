import sqlite3 as sql

conexao = sql.connect("livraria.db")
cursor = conexao.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS livros (
                livro_id integer primary key autoincrement,
                Titulo VARCHAR(100) not null,
                Autor VARCHAR(100) not null,
                Categoria VARCHAR(50) not null,
                Preco decimal(6,2),
                Quantidade VARCHAR(50) not null)
                """)

conexao.commit()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS Vendas (
                Venda_id integer primary key autoincrement,
                livro_id integer(50) not null,
                Preco_unit decimal(10,2),
                Date text not null,
                foreign key (livro_id) references livros(livro_id))
                """)
                

conexao.commit()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS Usuarios (
                usuario varchar(30) primary key,
                senha varchar(100) not null)
                """)

                
conexao.commit()


#   FUNÇÕES PARA O TKINTER (C.R.U.D)


# Para adicionar algum livro 
def adicionarLivro(titulo, autor, categoria, preco, quantidade):

    cursor.execute("""
        INSERT INTO livros (Titulo, Autor, Categoria, Preco, Quantidade)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, autor, categoria, preco, quantidade))
    print("Terceiro def")

    conexao.commit()



# Para deletar algum livro
def deletarLivro(livro_id):

    cursor.execute("""
        delete from livros where livro_id = ?
    """, (livro_id,))
    print("Terceiro def")

    conexao.commit()



# Para buscar algum livro(ou livros)
def buscarLivro(livro):

    cursor.execute("""
        SELECT * FROM livros
        WHERE CAST(livro_id AS TEXT) LIKE ?
           OR autor LIKE ?
           OR titulo LIKE ?
    """, (f"%{livro}%", f"%{livro}%", f"%{livro}%"))

    livrosBusc = cursor.fetchall()
    print("3")

    return livrosBusc


#PAra atualizar algum livro
def atualizarLivro(Titulo=None, Autor=None, Categoria=None, Preco=None, Quantidade=None, livro_id=None):

    Titulo = Titulo  if Titulo else None
    Autor = Autor  if Autor else None
    Categoria = Categoria  if Categoria else None
    Preco = Preco  if Preco else None
    Quantidade = Quantidade  if Quantidade else None

    cursor.execute("""
        update livros
        set Titulo = COALESCE(?, Titulo),
            Autor = COALESCE(?, Autor),
            Categoria = COALESCE(?, Categoria),
            Preco = COALESCE(?, Preco),
            Quantidade = COALESCE(?, Quantidade)
        where livro_id = ?
    """, (Titulo, Autor, Categoria, Preco, Quantidade,livro_id))

    conexao.commit()

def verificarLogin(usuario,senha):
    cursor.execute("""
    SELECT EXISTS (
    SELECT 1
    FROM Usuarios
    WHERE usuario = ?
        and senha = ?) as login_valido
        """, (usuario,senha))
    
    Resultado = cursor.fetchone()
    return Resultado[0]



