from sql import adicionarLivro, deletarLivro, buscarLivro, atualizarLivro, verificarLogin, verificarTipoLogin, buscarLivroVenda, Venderlivro, adicionarHisto

def adicionar_Livro(titulo, autor, categoria, preco, quantidade):
    adicionarLivro(titulo, autor, categoria, preco, quantidade)


def deletar_livro(livro_id):
    deletarLivro(livro_id)
    

def Buscar_Livro(livro):

    resultado = buscarLivro(livro)
    return resultado

def  Atualizar_livro(titulo, autor, categoria, preco, quantidade, id):
    atualizarLivro(titulo, autor, categoria, preco, quantidade, id)
    print("Segunda def")


def verificar_login(usuario,senha):
    resultado = verificarLogin(usuario,senha)
    return resultado

def Verificar_Tipo_Login(usuario):
    resultado = verificarTipoLogin(usuario)
    return resultado

def Buscar_Livro_venda(livro_id):
    resultado = buscarLivroVenda(livro_id)
    return resultado

def Vender_livro(livro_id):
    Venderlivro(livro_id)


def adicionar_Histo():
    adicionarHisto()

