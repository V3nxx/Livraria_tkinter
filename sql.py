import sqlite3 as sql
from datetime import datetime

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


# Garante a coluna do vendedor na tabela Vendas
# (tambem atualiza o banco livraria.db que ja foi criado antes)
colunas_vendas = [c[1] for c in cursor.execute("PRAGMA table_info(Vendas)").fetchall()]

if "Vendedor_id" not in colunas_vendas:
    cursor.execute("ALTER TABLE Vendas ADD COLUMN Vendedor_id varchar(30)")
    conexao.commit()

# Compra_id agrupa os livros de uma mesma venda (e e o "ID da venda" do historico)
if "Compra_id" not in colunas_vendas:
    cursor.execute("ALTER TABLE Vendas ADD COLUMN Compra_id integer")
    cursor.execute("UPDATE Vendas SET Compra_id = Venda_id")   # vendas antigas: 1 livro = 1 venda
    conexao.commit()

# Cancelada: 0 = venda concluida, 1 = venda cancelada
if "Cancelada" not in colunas_vendas:
    cursor.execute("ALTER TABLE Vendas ADD COLUMN Cancelada integer NOT NULL DEFAULT 0")
    conexao.commit()


cursor.execute("""
                CREATE TABLE IF NOT EXISTS Usuarios (
                usuario varchar(30) primary key,
                senha varchar(100) not null,
                tipo varchar(100) not null)
                """)
conexao.commit()


cursor.execute("""
                CREATE TABLE IF NOT EXISTS Vendedor (
                Funcionario varchar(30) primary key,
                usuario varchar(100) not null)
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


# Para atualizar algum livro


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

def verificarTipoLogin(usuario):
    cursor.execute("""
    select tipo from Usuarios
    where usuario = ?""",(usuario,))

    Resultado = cursor.fetchone()
    return Resultado[0]

def buscarLivroVenda(livro_id):
    cursor.execute("""
        SELECT * FROM livros
        WHERE livro_id = ?
    """, (livro_id,))

    resultado = cursor.fetchone()
    print("3")

    return resultado

def verificarTipoLogin(usuario):
    cursor.execute("""
    select tipo from Usuarios
    where usuario = ?""",(usuario,))

    Resultado = cursor.fetchone()
    return Resultado[0]

def Venderlivro(livro_id):
    cursor.execute("""
    update livros
        set Quantidade = Quantidade - 1
        where livro_id = ?
    """,(livro_id,))

    conexao.commit()

# Gera o id da proxima venda (todos os livros da mesma venda usam o mesmo id)


def novaCompraId():

    cursor.execute("SELECT COALESCE(MAX(Compra_id), 0) + 1 FROM Vendas")

    return cursor.fetchone()[0]


# Para salvar uma venda no historico (uma linha por livro vendido)


def adicionarHisto(livro_id, Preco_unit, Vendedor_id, Compra_id):

    Date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO Vendas (livro_id, Preco_unit, Date, Vendedor_id, Compra_id)
    VALUES (?, ?, ?, ?, ?)
    """, (livro_id, Preco_unit, Date, Vendedor_id, Compra_id))

    conexao.commit()


# Para cancelar uma venda: devolve os livros ao estoque e marca como cancelada


def cancelarVenda(compra_id):

    cursor.execute("""
        SELECT livro_id FROM Vendas
        WHERE Compra_id = ? AND Cancelada = 0
    """, (compra_id,))

    itens = cursor.fetchall()

    for (livro_id,) in itens:
        cursor.execute("""
            UPDATE livros
            SET Quantidade = Quantidade + 1
            WHERE livro_id = ?
        """, (livro_id,))

    cursor.execute("""
        UPDATE Vendas SET Cancelada = 1 WHERE Compra_id = ?
    """, (compra_id,))

    conexao.commit()


# Converte o que o usuario digitou para o formato salvo no banco (aaaa-mm-dd)
# Aceita: dd/mm/aaaa (dia), mm/aaaa (mes) ou aaaa (ano)


def normalizarData(texto):

    texto = texto.strip().replace("-", "/")
    partes = texto.split("/")

    try:
        if len(partes) == 3:
            if len(partes[0]) == 4:
                ano, mes, dia = partes
            else:
                dia, mes, ano = partes
            return f"{int(ano):04d}-{int(mes):02d}-{int(dia):02d}"

        if len(partes) == 2:
            if len(partes[0]) == 4:
                ano, mes = partes
            else:
                mes, ano = partes
            return f"{int(ano):04d}-{int(mes):02d}"

    except ValueError:
        pass

    return texto


# Para buscar no historico (filtros vazios = traz tudo)
# Cada venda volta com: id, vendedor, total, data, status e a lista de livros


def buscarHistorico(venda_id="", data="", vendedor=""):

    consulta = """
        SELECT v.Compra_id,
               v.Vendedor_id,
               printf('R$ %.2f', SUM(v.Preco_unit)),
               strftime('%d/%m/%Y %H:%M', MIN(v.Date)),
               CASE WHEN MAX(v.Cancelada) = 1 THEN 'Cancelada' ELSE 'Concluída' END
        FROM Vendas v
        WHERE 1 = 1
    """
    parametros = []

    if venda_id:
        consulta += " AND v.Compra_id = ?"
        parametros.append(venda_id)

    if vendedor:
        consulta += " AND v.Vendedor_id LIKE ?"
        parametros.append(f"%{vendedor}%")

    consulta += " GROUP BY v.Compra_id"

    if data:
        consulta += " HAVING MIN(v.Date) LIKE ?"
        parametros.append(f"{normalizarData(data)}%")

    consulta += " ORDER BY v.Compra_id DESC"

    cursor.execute(consulta, parametros)
    vendas = cursor.fetchall()

    resultado = []

    for compra_id, vendedor_id, total, data_venda, status in vendas:

        cursor.execute("""
            SELECT COALESCE(l.Titulo, '(livro removido)'),
                   printf('R$ %.2f', v.Preco_unit)
            FROM Vendas v
            LEFT JOIN livros l ON l.livro_id = v.livro_id
            WHERE v.Compra_id = ?
            ORDER BY v.Venda_id
        """, (compra_id,))

        livros = cursor.fetchall()

        resultado.append((compra_id, vendedor_id, total, data_venda, status, livros))

    return resultado


def adicionarUser(usuario, senha, tipo):
    cursor.execute("""
    insert into usuarios ( usuario, senha, tipo)
    values (?, ?, ?)
""", (usuario, senha, tipo))

    conexao.commit()