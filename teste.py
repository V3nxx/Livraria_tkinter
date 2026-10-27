import tkinter as tk
from tkinter import ttk
from main import adicionar_Livro, deletar_livro, Buscar_Livro, Atualizar_livro, verificar_login, Verificar_Tipo_Login, Buscar_Livro_venda, Vender_livro

# FUNÇÕES 


    # FLUXO DE PAGINAS

def voltar():
    print("ok")
    Addframe.pack_forget()
    delFrame.pack_forget()
    BuscFrame.pack_forget()
    UpdFrame.pack_forget()
    VendaFrame.pack_forget()
    main.pack()
    
def menuHist():
    main.pack_forget()
    histFrame.pack()
    print("ok")

def menuAdd():
    main.pack_forget()
    Addframe.pack()

def menuDel():
    main.pack_forget()
    delFrame.pack()

def menuBusc():
    main.pack_forget()
    BuscFrame.pack()

def menuUpd():
    main.pack_forget()
    UpdFrame.pack()

def menuVenda():
    main.pack_forget()
    VendaFrame.pack()

    # BOTÕES DAS PAGINAS
def VerificarLogin():
    usuario = Usuario.get()
    senha = Senha.get()
    resultado = verificar_login(usuario,senha)
    if resultado == 1:

        resultado = Verificar_Tipo_Login(usuario)

        if resultado == "Admin":
            main.pack()
            loginFrame.pack_forget()
            tk.Button(main, text="Cadastrar", command=menuAdd).pack()
            tk.Button(main, text="Deletar", command=menuDel).pack()
            tk.Button(main, text="Buscar", command=menuBusc).pack()
            tk.Button(main, text="Atualizar Cadastro", command=menuUpd).pack()
            tk.Button(main, text="Historico de vendas", command=menuHist).pack()

        elif resultado == "Funcionario":
            main.pack()
            loginFrame.pack_forget()
            tk.Button(main, text="Buscar", command=menuBusc).pack()
            tk.Button(main, text="Venda", command=menuVenda).pack()

        elif resultado == "Gerente":
            main.pack()
            loginFrame.pack_forget()
            tk.Button(main, text="Cadastrar", command=menuAdd).pack()
            tk.Button(main, text="Deletar", command=menuDel).pack()
            tk.Button(main, text="Buscar", command=menuBusc).pack()
            tk.Button(main, text="Atualizar Cadastro", command=menuUpd).pack()
            tk.Button(main, text="Historico de vendas", command=menuHist).pack()

    else:
        print("senha ou usuario incorreto")



def addLivro():

    titulo = TituloAdd.get()
    autor = AutorAdd.get()
    categoria = CategAdd.get()
    preco = PrecoAdd.get()
    quantidade = QuantAdd.get()
    Addframe.pack_forget()
    main.pack()

    adicionar_Livro(titulo,autor,categoria,preco,quantidade)

def updLivro():

    titulo = TituloUpd.get()
    autor = AutorUpd.get()
    categoria = CategUpd.get()
    preco = PrecoUpd.get()
    quantidade = QuantUpd.get()
    id = IdUpd.get()
    UpdFrame.pack_forget()
    main.pack()

    Atualizar_livro(titulo,autor,categoria,preco,quantidade,id)

def delLivro():

    livro_id = LivroDel.get()
    delFrame.pack_forget()
    main.pack()

    deletar_livro(livro_id)

def BuscarL():

    Livro = barraBusca.get()

    resultados = Buscar_Livro(Livro)

    # Limpa os resultados anteriores
    for item in TabelaLivro.get_children():
        TabelaLivro.delete(item)

    # Insere os livros encontrados
    for registro in resultados:
        TabelaLivro.insert("", tk.END, values=registro)
    print("1")

def Venderlivro():
    for item in TabelaLivroVenda.get_children():
        livro = TabelaLivroVenda.item(item, "values")

        livro_id = livro[0]
        Vender_livro(livro_id)


def BuscaVenda(idVenda):
    livro_id = idVenda.get()
    Precos = 0
    resultados = Buscar_Livro_venda(livro_id)
    if resultados:
        TabelaLivroVenda.insert("", tk.END, values=resultados)
        Valortotal(resultados)
    else:
        print("Erro, ID errado")

precoTotal = 0

def Valortotal(resultados):
    global precoTotal

    valor = resultados[4]
    precoTotal += valor

    ValorTotal.config(text=f"Total: R$ {precoTotal:.2f}")



# JANELA PRINCIPAL

janela = tk.Tk()
janela.title("Login")
janela.geometry("800x300")

# FRAME DE LOGIN

loginFrame = tk.Frame(janela)
loginFrame.pack()
Usuario = tk.Entry(loginFrame)
Usuario.pack()
Senha = tk.Entry(loginFrame)
Senha.pack()
tk.Button(loginFrame, text="Entrar", command=VerificarLogin).pack()

# FRAME PRINCIPAL

main = tk.Frame(janela)



# FRAME DA ADIÇÃO

Addframe = tk.Frame(janela)

tk.Label(Addframe, text="Nome do livro:").pack()
TituloAdd = tk.Entry(Addframe)
TituloAdd.pack()

tk.Label(Addframe, text="Nome do autor:").pack()
AutorAdd = tk.Entry(Addframe)
AutorAdd.pack()

tk.Label(Addframe, text="Categoria:").pack()
CategAdd = tk.Entry(Addframe)
CategAdd.pack()

tk.Label(Addframe, text="Preço:").pack()
PrecoAdd = tk.Entry(Addframe)
PrecoAdd.pack()

tk.Label(Addframe, text="Quantidade:").pack()
QuantAdd = tk.Entry(Addframe)
QuantAdd.pack()

Add = tk.Button(Addframe, text="Adicionar", command = addLivro)
Add.pack()

Btvoltar = tk.Button(Addframe, text="voltar", command = voltar)
Btvoltar.pack()


# REMOVER LIVRO

delFrame = tk.Frame(janela)

tk.Label(delFrame, text="Id / Nome do livro:").pack()
LivroDel = tk.Entry(delFrame)
LivroDel.pack()

Del = tk.Button(delFrame, text="Deletar", command = delLivro)
Del.pack()

Btvoltar = tk.Button(delFrame, text="voltar", command = voltar)
Btvoltar.pack()


# BUSCAR LIVRO 

BuscFrame = tk.Frame(janela)

barraBusca = tk.Entry(BuscFrame)
barraBusca.pack()

BotaoBusc = tk.Button(BuscFrame,text="Buscar", command=BuscarL)
BotaoBusc.pack()

Btvoltar = tk.Button(BuscFrame, text="voltar", command = voltar)
Btvoltar.pack()

# FRAME VENDA
VendaFrame = tk.Frame(janela)

idVenda = tk.Entry(VendaFrame)
idVenda.pack()

Btvoltar = tk.Button(VendaFrame, text="voltar", command = voltar)
Btvoltar.pack()

BuscarLivroVenda = tk.Button(VendaFrame,text="Buscar", command=lambda: BuscaVenda(idVenda))
BuscarLivroVenda.pack()

ValorTotal = tk.Label(VendaFrame, text="Total: R$ 0.00")
ValorTotal.pack()

BotaoVend = tk.Button(VendaFrame,text="Vender", command =Venderlivro)
BotaoVend.pack()

TabelaLivroVenda = ttk.Treeview(
    VendaFrame,
    columns=("ID","TITULO","AUTOR","CATEGORIA","PREÇO","QUANTIDADE"),
    show="headings"
)
TabelaLivroVenda.pack()

TabelaLivroVenda.heading("ID", text="ID")
TabelaLivroVenda.heading("TITULO", text="TITULO")
TabelaLivroVenda.heading("AUTOR", text="AUTOR")
TabelaLivroVenda.heading("CATEGORIA", text="CATEGORIA")
TabelaLivroVenda.heading("PREÇO", text="PREÇO")
TabelaLivroVenda.heading("QUANTIDADE", text="QUANTIDADE")

TabelaLivroVenda.column("ID",width=50) 
TabelaLivroVenda.column("TITULO", width=200)
TabelaLivroVenda.column("AUTOR", width=150)
TabelaLivroVenda.column("CATEGORIA", width=120 )
TabelaLivroVenda.column("PREÇO", width=100)
TabelaLivroVenda.column("QUANTIDADE", width=100)

    # Tabela

TabelaLivro = ttk.Treeview(
    BuscFrame,
    columns=("ID","TITULO","AUTOR","CATEGORIA","PREÇO","QUANTIDADE"),
    show="headings"
)
TabelaLivro.pack()

TabelaLivro.heading("ID", text="ID")
TabelaLivro.heading("TITULO", text="TITULO")
TabelaLivro.heading("AUTOR", text="AUTOR")
TabelaLivro.heading("CATEGORIA", text="CATEGORIA")
TabelaLivro.heading("PREÇO", text="PREÇO")
TabelaLivro.heading("QUANTIDADE", text="QUANTIDADE")

TabelaLivro.column("ID",width=50) 
TabelaLivro.column("TITULO", width=200)
TabelaLivro.column("AUTOR", width=150)
TabelaLivro.column("CATEGORIA", width=120 )
TabelaLivro.column("PREÇO", width=100)
TabelaLivro.column("QUANTIDADE", width=100)


# atualizar cadastro

UpdFrame = tk.Frame(janela)

tk.Label(UpdFrame, text="Nome do livro:").pack()
TituloUpd = tk.Entry(UpdFrame)
TituloUpd.pack()

tk.Label(UpdFrame, text="Nome do autor:").pack()
AutorUpd = tk.Entry(UpdFrame)
AutorUpd.pack()

tk.Label(UpdFrame, text="Categoria:").pack()
CategUpd = tk.Entry(UpdFrame)
CategUpd.pack()

tk.Label(UpdFrame, text="Preço:").pack()
PrecoUpd = tk.Entry(UpdFrame)
PrecoUpd.pack()

tk.Label(UpdFrame, text="Quantidade:").pack()
QuantUpd = tk.Entry(UpdFrame)
QuantUpd.pack()

tk.Label(UpdFrame, text="ID:").pack()
IdUpd = tk.Entry(UpdFrame)
IdUpd.pack()

Upd = tk.Button(UpdFrame, text="Atualizar", command = updLivro)
Upd.pack()

Btvoltar = tk.Button(UpdFrame, text="voltar", command = voltar)
Btvoltar.pack()

# HISTORICO DE VENDAS

histFrame = tk.Frame(janela)

TabelaLivroHisto = ttk.Treeview(
    histFrame,
    columns=("ID","ID_Vendedor","TITULOS","PRECO_TOTAL","DATA"),
    show="headings"
)
TabelaLivroHisto.pack()

TabelaLivroHisto.heading("ID", text="ID")
TabelaLivroHisto.heading("ID_Vendedor", text="ID_Vendedor")
TabelaLivroHisto.heading("TITULOS", text="TITULOS")
TabelaLivroHisto.heading("PRECO_TOTAL", text="PRECO TOTAL")
TabelaLivroHisto.heading("DATA", text="DATA")

TabelaLivroHisto.column("ID", width=50 )
TabelaLivroHisto.column("ID_Vendedor", width=50 )
TabelaLivroHisto.column("TITULOS", width=200)
TabelaLivroHisto.column("PRECO_TOTAL", width=50 )
TabelaLivroHisto.column("DATA", width=50)

janela.mainloop()