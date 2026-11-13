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


# Garante as colunas extras da tabela Vendas
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

# Titulo: copia do nome do livro salva na propria venda,
# assim o historico continua mostrando o nome mesmo se o livro for deletado
if "Titulo" not in colunas_vendas:
    cursor.execute("ALTER TABLE Vendas ADD COLUMN Titulo varchar(100)")
    cursor.execute("""
        UPDATE Vendas
        SET Titulo = (SELECT l.Titulo FROM livros l WHERE l.livro_id = Vendas.livro_id)
    """)   # vendas antigas: preenche com o titulo atual (se o livro ainda existir)
    conexao.commit()

# Qtd: quantas unidades do livro foram vendidas nessa linha
if "Qtd" not in colunas_vendas:
    cursor.execute("ALTER TABLE Vendas ADD COLUMN Qtd integer NOT NULL DEFAULT 1")
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


# Conversores usados quando o valor vem do banco (pode estar como texto)


def _para_float(valor):

    try:
        return float(str(valor).replace(",", "."))
    except (TypeError, ValueError):
        return 0.0


def _para_int(valor):

    try:
        return int(float(valor))
    except (TypeError, ValueError):
        return 0


#   FUNÇÕES PARA O TKINTER (C.R.U.D)


# Para adicionar algum livro


def adicionarLivro(titulo, autor, categoria, preco, quantidade):

    cursor.execute("""
        INSERT INTO livros (Titulo, Autor, Categoria, Preco, Quantidade)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, autor, categoria, preco, quantidade))

    conexao.commit()


# Para deletar algum livro (devolve quantos livros foram apagados)


def deletarLivro(livro_id):

    cursor.execute("""
        delete from livros where livro_id = ?
    """, (livro_id,))

    conexao.commit()

    return cursor.rowcount


# Para buscar algum livro(ou livros)


def buscarLivro(livro):

    cursor.execute("""
        SELECT * FROM livros
        WHERE CAST(livro_id AS TEXT) LIKE ?
           OR autor LIKE ?
           OR titulo LIKE ?
    """, (f"%{livro}%", f"%{livro}%", f"%{livro}%"))

    return cursor.fetchall()


# Para atualizar algum livro (campos None continuam como estavam)
# Devolve quantos livros foram atualizados (0 = ID nao existe)


def atualizarLivro(titulo, autor, categoria, preco, quantidade, livro_id):

    cursor.execute("""
        update livros
        set Titulo = COALESCE(?, Titulo),
            Autor = COALESCE(?, Autor),
            Categoria = COALESCE(?, Categoria),
            Preco = COALESCE(?, Preco),
            Quantidade = COALESCE(?, Quantidade)
        where livro_id = ?
    """, (titulo, autor, categoria, preco, quantidade, livro_id))

    conexao.commit()

    return cursor.rowcount


def verificarLogin(usuario, senha):

    cursor.execute("""
    SELECT EXISTS (
    SELECT 1
    FROM Usuarios
    WHERE usuario = ?
        and senha = ?) as login_valido
        """, (usuario, senha))

    return cursor.fetchone()[0]


def verificarTipoLogin(usuario):

    cursor.execute("""
    select tipo from Usuarios
    where usuario = ?""", (usuario,))

    resultado = cursor.fetchone()

    return resultado[0] if resultado else None


def buscarLivroVenda(livro_id):

    cursor.execute("""
        SELECT * FROM livros
        WHERE livro_id = ?
    """, (livro_id,))

    return cursor.fetchone()


# Gera o id da proxima venda (todos os livros da mesma venda usam o mesmo id)


def novaCompraId():

    cursor.execute("SELECT COALESCE(MAX(Compra_id), 0) + 1 FROM Vendas")

    return cursor.fetchone()[0]


# Para registrar uma venda inteira de uma vez
# itens = [(livro_id, quantidade), ...]
# Confere o estoque de TODOS antes de vender qualquer coisa. Se faltar estoque,
# nada e vendido. Tudo (baixa no estoque + historico) acontece numa transacao so.
# Devolve (True, (compra_id, total)) ou (False, [lista de problemas])


def registrarVenda(itens, vendedor_id):

    try:

        problemas = []
        validos = []

        for livro_id, qtd in itens:

            cursor.execute("""
                SELECT Titulo, Preco, Quantidade FROM livros
                WHERE livro_id = ?
            """, (livro_id,))

            livro = cursor.fetchone()

            if livro is None:
                problemas.append(f"O livro de ID {livro_id} não existe mais")
                continue

            titulo, preco, estoque = livro
            estoque = _para_int(estoque)

            if estoque < qtd:
                problemas.append(f"{titulo} (pedido: {qtd}, em estoque: {estoque})")
            else:
                validos.append((livro_id, titulo, _para_float(preco), qtd))

        if problemas:
            return False, problemas

        compra_id = novaCompraId()
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = 0.0

        for livro_id, titulo, preco, qtd in validos:

            cursor.execute("""
                UPDATE livros
                SET Quantidade = Quantidade - ?
                WHERE livro_id = ?
            """, (qtd, livro_id))

            cursor.execute("""
                INSERT INTO Vendas (livro_id, Titulo, Preco_unit, Qtd, Date, Vendedor_id, Compra_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (livro_id, titulo, preco, qtd, data, vendedor_id, compra_id))

            total += preco * qtd

        conexao.commit()

        return True, (compra_id, total)

    except sql.Error:

        conexao.rollback()

        return False, ["Erro ao gravar a venda no banco de dados."]


# Para cancelar uma venda: devolve os livros ao estoque e marca como cancelada


def cancelarVenda(compra_id):

    cursor.execute("""
        SELECT livro_id, Qtd FROM Vendas
        WHERE Compra_id = ? AND Cancelada = 0
    """, (compra_id,))

    itens = cursor.fetchall()

    for livro_id, qtd in itens:
        cursor.execute("""
            UPDATE livros
            SET Quantidade = Quantidade + ?
            WHERE livro_id = ?
        """, (qtd, livro_id))

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
# (cada livro: titulo, quantidade, preco unitario)


def buscarHistorico(venda_id="", data="", vendedor=""):

    consulta = """
        SELECT v.Compra_id,
               v.Vendedor_id,
               printf('R$ %.2f', SUM(v.Preco_unit * v.Qtd)),
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

        # usa o titulo salvo na venda; so cai no livro atual / "removido" em vendas muito antigas
        cursor.execute("""
            SELECT COALESCE(v.Titulo, l.Titulo, '(livro removido)'),
                   v.Qtd,
                   printf('R$ %.2f', v.Preco_unit)
            FROM Vendas v
            LEFT JOIN livros l ON l.livro_id = v.livro_id
            WHERE v.Compra_id = ?
            ORDER BY v.Venda_id
        """, (compra_id,))

        livros = cursor.fetchall()

        resultado.append((compra_id, vendedor_id, total, data_venda, status, livros))

    return resultado


#   USUARIOS


# Devolve True se cadastrou, False se o usuario ja existe


def adicionarUser(usuario, senha, tipo):

    try:
        cursor.execute("""
            INSERT INTO Usuarios (usuario, senha, tipo)
            VALUES (?, ?, ?)
        """, (usuario, senha, tipo))

        conexao.commit()

        return True

    except sql.IntegrityError:

        conexao.rollback()

        return False


# A senha nunca volta na listagem


def listarUsuarios():

    cursor.execute("SELECT usuario, tipo FROM Usuarios ORDER BY usuario")

    return cursor.fetchall()


# senha None = mantem a senha atual


def atualizarUsuario(usuario, senha, tipo):

    cursor.execute("""
        UPDATE Usuarios
        SET senha = COALESCE(?, senha),
            tipo = ?
        WHERE usuario = ?
    """, (senha, tipo, usuario))

    conexao.commit()

    return cursor.rowcount


def removerUsuario(usuario):

    cursor.execute("DELETE FROM Usuarios WHERE usuario = ?", (usuario,))

    conexao.commit()

    return cursor.rowcount


def contarAdmins():

    cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE tipo = 'Admin'")

    return cursor.fetchone()[0]


def existeAdmin():

    return contarAdmins() > 0
