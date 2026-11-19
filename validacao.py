import re

from sql import (
    adicionarLivro, deletarLivro, buscarLivro, atualizarLivro,
    verificarLogin, verificarTipoLogin, buscarLivroVenda, registrarVenda,
    buscarHistorico, cancelarVenda,
    adicionarUser, listarUsuarios, atualizarUsuario, removerUsuario,
    contarAdmins, existeAdmin,
)

TIPOS_USUARIO = ("Admin", "Gerente", "Funcionario")


# ==========================================
# VALIDAÇÕES (devolvem None se o texto não for número válido)
# ==========================================

def _preco(texto):

    texto = str(texto).strip().replace(",", ".")

    if not re.fullmatch(r"[0-9]+(\.[0-9]{1,2})?", texto):
        return None

    return round(float(texto), 2)


def _inteiro(texto):

    texto = str(texto).strip()

    if not re.fullmatch(r"[0-9]+", texto):
        return None

    return int(texto)


# ==========================================
# LIVROS
# Quem pode falhar devolve (True, "") ou (False, "mensagem para o usuário")
# ==========================================

def adicionar_Livro(titulo, autor, categoria, preco, quantidade):

    titulo = titulo.strip()
    autor = autor.strip()
    categoria = categoria.strip()

    if not (titulo and autor and categoria):
        return False, "Preencha o título, o autor e a categoria."

    preco_num = _preco(preco)
    if preco_num is None:
        return False, "O preço deve ser um número (exemplo: 29.90)."

    quantidade_num = _inteiro(quantidade)
    if quantidade_num is None:
        return False, "A quantidade deve ser um número inteiro."

    adicionarLivro(titulo, autor, categoria, preco_num, quantidade_num)

    return True, ""


def deletar_livro(livro_id):

    livro_id = _inteiro(livro_id)
    if livro_id is None:
        return False, "Digite o ID do livro (somente números)."

    if deletarLivro(livro_id) == 0:
        return False, f"Nenhum livro encontrado com o ID {livro_id}."

    return True, ""


def Buscar_Livro(livro):

    return buscarLivro(livro)


def Atualizar_livro(titulo, autor, categoria, preco, quantidade, livro_id):

    livro_id = _inteiro(livro_id)
    if livro_id is None:
        return False, "Digite o ID do livro que será atualizado (somente números)."

    titulo = titulo.strip() or None
    autor = autor.strip() or None
    categoria = categoria.strip() or None

    preco_num = None
    if preco.strip():
        preco_num = _preco(preco)
        if preco_num is None:
            return False, "O preço deve ser um número (exemplo: 29.90)."

    quantidade_num = None
    if quantidade.strip():
        quantidade_num = _inteiro(quantidade)
        if quantidade_num is None:
            return False, "A quantidade deve ser um número inteiro."

    if all(v is None for v in (titulo, autor, categoria, preco_num, quantidade_num)):
        return False, "Preencha pelo menos um campo para atualizar."

    if atualizarLivro(titulo, autor, categoria, preco_num, quantidade_num, livro_id) == 0:
        return False, f"Nenhum livro encontrado com o ID {livro_id}."

    return True, ""


# ==========================================
# LOGIN
# ==========================================

def verificar_login(usuario, senha):

    return verificarLogin(usuario, senha)


def Verificar_Tipo_Login(usuario):

    return verificarTipoLogin(usuario)


# ==========================================
# VENDAS
# ==========================================

def Buscar_Livro_venda(livro_id):

    return buscarLivroVenda(livro_id)


# itens = [(livro_id, quantidade), ...]
# Devolve (True, (compra_id, total)) ou (False, [problemas])

def Finalizar_Venda(itens, vendedor):

    return registrarVenda(itens, vendedor)


def Cancelar_Venda(compra_id):

    cancelarVenda(compra_id)


def Buscar_Historico(venda_id, data, vendedor):

    return buscarHistorico(venda_id, data, vendedor)


# ==========================================
# USUÁRIOS
# ==========================================

def existe_admin():

    return existeAdmin()


def listar_usuarios():

    return listarUsuarios()


def adicionar_usuario(usuario, senha, tipo):

    usuario = usuario.strip()

    if not usuario or not senha:
        return False, "Preencha o usuário e a senha."

    if tipo not in TIPOS_USUARIO:
        return False, "Tipo de usuário inválido."

    if not adicionarUser(usuario, senha, tipo):
        return False, f"O usuário '{usuario}' já existe."

    return True, ""


# senha vazia = mantém a senha atual

def atualizar_usuario(usuario, senha, tipo):

    if tipo not in TIPOS_USUARIO:
        return False, "Tipo de usuário inválido."

    tipo_atual = verificarTipoLogin(usuario)

    if tipo_atual is None:
        return False, "Usuário não encontrado."

    if tipo_atual == "Admin" and tipo != "Admin" and contarAdmins() <= 1:
        return False, "Este é o único administrador. Crie outro antes de mudar o tipo dele."

    atualizarUsuario(usuario, senha or None, tipo)

    return True, ""


def remover_usuario(usuario, usuario_logado):

    if usuario == usuario_logado:
        return False, "Você não pode remover o usuário com o qual está logado."

    tipo = verificarTipoLogin(usuario)

    if tipo is None:
        return False, "Usuário não encontrado."

    if tipo == "Admin" and contarAdmins() <= 1:
        return False, "Este é o único administrador e não pode ser removido."

    removerUsuario(usuario)

    return True, ""
