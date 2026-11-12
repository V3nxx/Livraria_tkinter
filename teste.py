
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from main import (
    adicionar_Livro,
    deletar_livro,
    Buscar_Livro,
    Atualizar_livro,
    verificar_login,
    Verificar_Tipo_Login,
    Buscar_Livro_venda,
    Vender_livro,
    adicionar_Histo,
    Buscar_Historico,
    adicionar_usuario,
    Nova_Compra_Id,
    Cancelar_Venda
)

# ==========================================
# CONFIGURAÇÕES
# ==========================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FUNDO = "#f7f3ea"
BOTAO = "#FFFFFF"
LETRAS = "#244638"
HOVER = "#EAE6DC"

janela = ctk.CTk()
janela.title("Sistema de Livraria")
janela.attributes("-fullscreen", True)

# ESC para sair do fullscreen
janela.bind(
    "<Escape>",
    lambda event: janela.attributes("-fullscreen", False)
)


# ==========================================
# FUNÇÕES DE ESTILO
# ==========================================

def criar_botao(frame, texto, comando):

    return ctk.CTkButton(
        frame,
        text=texto,
        command=comando,
        width=250,
        height=45,
        corner_radius=10,
        fg_color=BOTAO,
        hover_color=HOVER,
        text_color=LETRAS,
        border_color=LETRAS,
        border_width=1,
        font=("Arial", 14, "bold")
    )


def criar_campo(frame, placeholder=""):

    return ctk.CTkEntry(
        frame,
        width=250,
        height=40,
        placeholder_text=placeholder,
        fg_color=BOTAO,
        text_color=LETRAS,
        border_color=LETRAS,
        corner_radius=8
    )


def criar_titulo(frame, texto):

    return ctk.CTkLabel(
        frame,
        text=texto,
        font=("Arial", 28, "bold"),
        text_color=LETRAS
    )


def mostrar_aviso(texto):

    aviso = ctk.CTkToplevel(janela)
    aviso.title("Aviso")
    aviso.geometry("400x200")
    aviso.configure(fg_color=FUNDO)
    aviso.attributes("-topmost", True)

    ctk.CTkLabel(
        aviso,
        text=texto,
        text_color=LETRAS,
        font=("Arial", 14),
        wraplength=350
    ).pack(pady=25, padx=20)

    criar_botao(
        aviso,
        "OK",
        aviso.destroy
    ).pack(pady=10)


# ==========================================
# FLUXO DE PÁGINAS
# ==========================================

def limpar_campos():

    # apaga tudo que foi digitado/listado, para nada ficar salvo ao trocar de tela
    campos = [
        Usuario, Senha,
        TituloAdd, AutorAdd, CategAdd, PrecoAdd, QuantAdd,
        LivroDel,
        barraBusca,
        idVenda,
        TituloUpd, AutorUpd, CategUpd, PrecoUpd, QuantUpd, IdUpd,
        idVendaHisto, dataHisto, vendedorHisto,
        UserAdd, SenhaAdd
    ]

    for campo in campos:
        campo.delete(0, "end")

    TipoAdd.set("Funcionario")

    for tabela in (TabelaLivro, TabelaLivroHisto):
        for item in tabela.get_children():
            tabela.delete(item)

    limpar_venda()

    loginErro.configure(text="")

    # tira o foco dos campos para o texto de exemplo (placeholder) voltar
    janela.focus()


def esconder_telas():

    limpar_campos()

    for frame in todas_telas:
        frame.pack_forget()


def voltar():

    esconder_telas()
    main.pack(fill="both", expand=True)


def menuHist():

    esconder_telas()
    PesquisarHisto()
    histFrame.pack(fill="both", expand=True)


def menuAdd():

    esconder_telas()
    Addframe.pack(fill="both", expand=True)


def menuDel():

    esconder_telas()
    delFrame.pack(fill="both", expand=True)


def menuBusc():

    esconder_telas()
    BuscFrame.pack(fill="both", expand=True)


def menuUpd():

    esconder_telas()
    UpdFrame.pack(fill="both", expand=True)


def menuVenda():

    esconder_telas()
    VendaFrame.pack(fill="both", expand=True)

def menuUser():

    esconder_telas()
    AddUser.pack(fill="both", expand=True)

# ==========================================
# MENU PRINCIPAL CENTRALIZADO
# ==========================================

def criar_menu():

    for widget in main.winfo_children():
        widget.destroy()

    # Frame que centraliza os elementos
    centro = ctk.CTkFrame(
        main,
        fg_color="transparent"
    )

    centro.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    criar_titulo(
        centro,
        "Sistema de Livraria"
    ).pack(pady=30)

    if tipo_usuario in ("Admin", "Gerente"):

        botoes = [
            ("Cadastrar", menuAdd),
            ("Deletar", menuDel),
            ("Buscar", menuBusc),
            ("Atualizar Cadastro", menuUpd),
            ("Historico de vendas", menuHist),
            ("Cadastrar usuario", menuUser)
        ]

    elif tipo_usuario == "Funcionario":

        botoes = [
            ("Buscar", menuBusc),
            ("Venda", menuVenda)
        ]

    else:
        return

    for texto, comando in botoes:

        criar_botao(
            centro,
            texto,
            comando
        ).pack(pady=8)

    criar_botao(
        centro,
        "Sair",
        logout
    ).pack(pady=8)


# ==========================================
# LOGIN
# ==========================================

def VerificarLogin():

    global tipo_usuario, usuario_logado

    usuario = Usuario.get()
    senha = Senha.get()

    resultado = verificar_login(usuario, senha)

    if resultado == 1:

        tipo_usuario = Verificar_Tipo_Login(usuario)
        usuario_logado = usuario

        esconder_telas()

        criar_menu()

        main.pack(fill="both", expand=True)

    else:

        loginErro.configure(
            text="Usuário ou senha incorretos!"
        )


# ==========================================
# LOGOUT
# ==========================================

def logout():

    global tipo_usuario, usuario_logado, precoTotal

    tipo_usuario = None
    usuario_logado = None
    precoTotal = 0

    # limpa os campos do login
    Usuario.delete(0, "end")
    Senha.delete(0, "end")
    loginErro.configure(text="")

    # limpa as tabelas e o total para o proximo usuario nao ver nada
    for tabela in (TabelaLivro, TabelaLivroVenda, TabelaLivroHisto):
        for item in tabela.get_children():
            tabela.delete(item)

    ValorTotal.configure(text="Total: R$ 0.00")

    esconder_telas()
    loginFrame.pack(fill="both", expand=True)


# ==========================================
# CADASTRAR LIVRO
# ==========================================

def addLivro():

    titulo = TituloAdd.get()
    autor = AutorAdd.get()
    categoria = CategAdd.get()
    preco = PrecoAdd.get()
    quantidade = QuantAdd.get()

    adicionar_Livro(
        titulo,
        autor,
        categoria,
        preco,
        quantidade
    )

    voltar()


# ==========================================
# ATUALIZAR LIVRO
# ==========================================

def updLivro():

    titulo = TituloUpd.get()
    autor = AutorUpd.get()
    categoria = CategUpd.get()
    preco = PrecoUpd.get()
    quantidade = QuantUpd.get()
    id = IdUpd.get()

    Atualizar_livro(
        titulo,
        autor,
        categoria,
        preco,
        quantidade,
        id
    )

    voltar()


# ==========================================
# DELETAR LIVRO
# ==========================================

def delLivro():

    livro_id = LivroDel.get()

    deletar_livro(livro_id)

    voltar()


# ==========================================
# BUSCAR LIVRO
# ==========================================

def BuscarL():

    Livro = barraBusca.get()

    resultados = Buscar_Livro(Livro)

    for item in TabelaLivro.get_children():
        TabelaLivro.delete(item)

    for registro in resultados:

        TabelaLivro.insert(
            "",
            tk.END,
            values=registro
        )


# ==========================================
# VENDAS
# ==========================================

precoTotal = 0


def BuscaVenda(idVenda):

    livro_id = idVenda.get()

    resultados = Buscar_Livro_venda(livro_id)

    if resultados:

        TabelaLivroVenda.insert(
            "",
            tk.END,
            values=resultados
        )

        Valortotal(resultados)

    else:

        print("Erro, ID errado")


def Valortotal(resultados):

    global precoTotal

    valor = float(resultados[4])

    precoTotal += valor

    ValorTotal.configure(
        text=f"Total: R$ {precoTotal:.2f}"
    )


def limpar_venda():

    global precoTotal

    for item in TabelaLivroVenda.get_children():
        TabelaLivroVenda.delete(item)

    precoTotal = 0

    ValorTotal.configure(
        text="Total: R$ 0.00"
    )


def Venderlivro():

    compra_id = None
    sem_estoque = []

    for item in TabelaLivroVenda.get_children():

        livro = TabelaLivroVenda.item(
            item,
            "values"
        )

        livro_id = livro[0]
        preco = float(livro[4])

        # confere o estoque atual no banco (vale tambem se o mesmo livro foi adicionado 2x)
        atual = Buscar_Livro_venda(livro_id)
        quantidade = int(atual[5]) if atual else 0

        if quantidade > 0:

            # todos os livros da mesma venda usam o mesmo id de venda
            if compra_id is None:
                compra_id = Nova_Compra_Id()

            Vender_livro(livro_id)

            # salva no historico: livro, preco unitario, quem vendeu e a venda
            adicionar_Histo(livro_id, preco, usuario_logado, compra_id)

        else:
            sem_estoque.append(livro[1])

    limpar_venda()

    if sem_estoque:
        mostrar_aviso("Não possui estoque do(s) livro(s): " + ", ".join(sem_estoque))


# ==========================================
# HISTÓRICO DE VENDAS (PESQUISA)
# ==========================================

def PesquisarHisto():

    venda_id = idVendaHisto.get().strip()
    data = dataHisto.get().strip()
    vendedor = vendedorHisto.get().strip()

    resultados = Buscar_Historico(venda_id, data, vendedor)

    for item in TabelaLivroHisto.get_children():
        TabelaLivroHisto.delete(item)

    for venda in resultados:

        compra_id, vendedor_id, total, data_venda, status, livros = venda

        tags = ("cancelada",) if status == "Cancelada" else ()

        # linha principal = a venda (com o valor total)
        pai = TabelaLivroHisto.insert(
            "",
            tk.END,
            values=(compra_id, f"{len(livros)} livro(s)", vendedor_id, "", total, data_venda, status),
            open=True,
            tags=tags
        )

        # linhas de baixo = cada livro da venda (com o preco unitario)
        for titulo, preco in livros:

            TabelaLivroHisto.insert(
                pai,
                tk.END,
                values=("", titulo, "", preco, "", "", ""),
                tags=tags
            )


def CancelarVendaHisto():

    selecao = TabelaLivroHisto.selection()

    if not selecao:
        mostrar_aviso("Selecione uma venda para cancelar.")
        return

    item = selecao[0]

    # se clicou em um livro, usa a venda dele
    pai = TabelaLivroHisto.parent(item)
    if pai:
        item = pai

    valores = TabelaLivroHisto.item(item, "values")

    compra_id = valores[0]
    status = valores[6]

    if status == "Cancelada":
        mostrar_aviso("Esta venda já foi cancelada.")
        return

    confirmar = messagebox.askyesno(
        "Cancelar venda",
        f"Cancelar a venda {compra_id}?\nOs livros voltam para o estoque."
    )

    if confirmar:
        Cancelar_Venda(compra_id)
        PesquisarHisto()


# ==========================================
# ADICIONAR USUARIO
# ==========================================

def addUser():
    usuario = UserAdd.get()
    senha = SenhaAdd.get()
    tipo = TipoAdd.get()

    adicionar_usuario(
        usuario,
        senha,
        tipo
    )

    voltar()



# ==========================================
# ESTILO DAS TABELAS
# ==========================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="#FFFFFF",
    foreground=LETRAS,
    fieldbackground="#FFFFFF",
    rowheight=30,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=LETRAS,
    foreground="#FFFFFF",
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#DCE8DF")],
    foreground=[("selected", LETRAS)]
)


# ==========================================
# FRAME DE LOGIN
# ==========================================

loginFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

loginFrame.pack(fill="both", expand=True)

loginCentro = ctk.CTkFrame(
    loginFrame,
    fg_color="transparent"
)

loginCentro.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

criar_titulo(
    loginCentro,
    "LIVRARIA"
).pack(pady=25)

ctk.CTkLabel(
    loginCentro,
    text="Faça login para continuar",
    text_color=LETRAS,
    font=("Arial", 16)
).pack(pady=10)

Usuario = criar_campo(
    loginCentro,
    "Usuário"
)
Usuario.pack(pady=8)

Senha = criar_campo(
    loginCentro,
    "Senha"
)
Senha.configure(show="*")
Senha.pack(pady=8)

criar_botao(
    loginCentro,
    "Entrar",
    VerificarLogin
).pack(pady=15)

loginErro = ctk.CTkLabel(
    loginCentro,
    text="",
    text_color="#B91C1C"
)
loginErro.pack()


# ==========================================
# FRAME PRINCIPAL
# ==========================================

main = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)


# ==========================================
# FRAME DA ADIÇÃO
# ==========================================

Addframe = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    Addframe,
    "Cadastrar Livro"
).pack(pady=20)

ctk.CTkLabel(Addframe, text="Nome do livro:", text_color=LETRAS).pack()
TituloAdd = criar_campo(Addframe)
TituloAdd.pack(pady=5)

ctk.CTkLabel(Addframe, text="Nome do autor:", text_color=LETRAS).pack()
AutorAdd = criar_campo(Addframe)
AutorAdd.pack(pady=5)

ctk.CTkLabel(Addframe, text="Categoria:", text_color=LETRAS).pack()
CategAdd = criar_campo(Addframe)
CategAdd.pack(pady=5)

ctk.CTkLabel(Addframe, text="Preço:", text_color=LETRAS).pack()
PrecoAdd = criar_campo(Addframe)
PrecoAdd.pack(pady=5)

ctk.CTkLabel(Addframe, text="Quantidade:", text_color=LETRAS).pack()
QuantAdd = criar_campo(Addframe)
QuantAdd.pack(pady=5)

criar_botao(
    Addframe,
    "Adicionar",
    addLivro
).pack(pady=8)

criar_botao(
    Addframe,
    "Voltar",
    voltar
).pack(pady=8)


# ==========================================
# REMOVER LIVRO
# ==========================================

delFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    delFrame,
    "Deletar Livro"
).pack(pady=25)

ctk.CTkLabel(
    delFrame,
    text="ID / Nome do livro:",
    text_color=LETRAS
).pack()

LivroDel = criar_campo(delFrame)
LivroDel.pack(pady=8)

criar_botao(
    delFrame,
    "Deletar",
    delLivro
).pack(pady=8)

criar_botao(
    delFrame,
    "Voltar",
    voltar
).pack(pady=8)


# ==========================================
# BUSCAR LIVRO
# ==========================================

BuscFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    BuscFrame,
    "Buscar Livros"
).pack(pady=20)

barraBusca = criar_campo(
    BuscFrame,
    "Nome do livro"
)
barraBusca.pack(pady=8)

criar_botao(
    BuscFrame,
    "Buscar",
    BuscarL
).pack(pady=8)

TabelaLivro = ttk.Treeview(
    BuscFrame,
    columns=("ID", "TITULO", "AUTOR", "CATEGORIA", "PREÇO", "QUANTIDADE"),
    show="headings"
)

TabelaLivro.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

for coluna in ("ID", "TITULO", "AUTOR", "CATEGORIA", "PREÇO", "QUANTIDADE"):
    TabelaLivro.heading(coluna, text=coluna)

TabelaLivro.column("ID", width=50)
TabelaLivro.column("TITULO", width=200)
TabelaLivro.column("AUTOR", width=150)
TabelaLivro.column("CATEGORIA", width=120)
TabelaLivro.column("PREÇO", width=100)
TabelaLivro.column("QUANTIDADE", width=100)

criar_botao(
    BuscFrame,
    "Voltar",
    voltar
).pack(pady=8)


# ==========================================
# FRAME VENDA
# ==========================================

VendaFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    VendaFrame,
    "Realizar Venda"
).pack(pady=20)

idVenda = criar_campo(
    VendaFrame,
    "ID do livro"
)
idVenda.pack(pady=8)

criar_botao(
    VendaFrame,
    "Buscar",
    lambda: BuscaVenda(idVenda)
).pack(pady=8)

ValorTotal = ctk.CTkLabel(
    VendaFrame,
    text="Total: R$ 0.00",
    text_color=LETRAS,
    font=("Arial", 18, "bold")
)
ValorTotal.pack(pady=10)

criar_botao(
    VendaFrame,
    "Vender",
    Venderlivro
).pack(pady=8)

criar_botao(
    VendaFrame,
    "Cancelar",
    limpar_venda
).pack(pady=8)

TabelaLivroVenda = ttk.Treeview(
    VendaFrame,
    columns=("ID", "TITULO", "AUTOR", "CATEGORIA", "PREÇO", "QUANTIDADE"),
    show="headings"
)

TabelaLivroVenda.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

for coluna in ("ID", "TITULO", "AUTOR", "CATEGORIA", "PREÇO", "QUANTIDADE"):
    TabelaLivroVenda.heading(coluna, text=coluna)

TabelaLivroVenda.column("ID", width=50)
TabelaLivroVenda.column("TITULO", width=200)
TabelaLivroVenda.column("AUTOR", width=150)
TabelaLivroVenda.column("CATEGORIA", width=120)
TabelaLivroVenda.column("PREÇO", width=100)
TabelaLivroVenda.column("QUANTIDADE", width=100)

criar_botao(
    VendaFrame,
    "Voltar",
    voltar
).pack(pady=8)


# ==========================================
# ATUALIZAR CADASTRO
# ==========================================

UpdFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    UpdFrame,
    "Atualizar Cadastro"
).pack(pady=20)

ctk.CTkLabel(UpdFrame, text="Nome do livro:", text_color=LETRAS).pack()
TituloUpd = criar_campo(UpdFrame)
TituloUpd.pack(pady=5)

ctk.CTkLabel(UpdFrame, text="Nome do autor:", text_color=LETRAS).pack()
AutorUpd = criar_campo(UpdFrame)
AutorUpd.pack(pady=5)

ctk.CTkLabel(UpdFrame, text="Categoria:", text_color=LETRAS).pack()
CategUpd = criar_campo(UpdFrame)
CategUpd.pack(pady=5)

ctk.CTkLabel(UpdFrame, text="Preço:", text_color=LETRAS).pack()
PrecoUpd = criar_campo(UpdFrame)
PrecoUpd.pack(pady=5)

ctk.CTkLabel(UpdFrame, text="Quantidade:", text_color=LETRAS).pack()
QuantUpd = criar_campo(UpdFrame)
QuantUpd.pack(pady=5)

ctk.CTkLabel(UpdFrame, text="ID:", text_color=LETRAS).pack()
IdUpd = criar_campo(UpdFrame)
IdUpd.pack(pady=5)

criar_botao(
    UpdFrame,
    "Atualizar",
    updLivro
).pack(pady=8)

criar_botao(
    UpdFrame,
    "Voltar",
    voltar
).pack(pady=8)


# ==========================================
# HISTÓRICO DE VENDAS
# ==========================================

histFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    histFrame,
    "Histórico de Vendas"
).pack(pady=25)

filtrosHisto = ctk.CTkFrame(
    histFrame,
    fg_color="transparent"
)

filtrosHisto.pack(pady=5)

idVendaHisto = criar_campo(
    filtrosHisto,
    "ID da venda"
)
idVendaHisto.configure(width=180)
idVendaHisto.pack(side="left", padx=5)

dataHisto = criar_campo(
    filtrosHisto,
    "Data: dd/mm/aaaa ou mm/aaaa"
)
dataHisto.configure(width=230)
dataHisto.pack(side="left", padx=5)

vendedorHisto = criar_campo(
    filtrosHisto,
    "Vendedor"
)
vendedorHisto.configure(width=180)
vendedorHisto.pack(side="left", padx=5)

btnPesquisarHisto = criar_botao(
    filtrosHisto,
    "Pesquisar",
    PesquisarHisto
)
btnPesquisarHisto.configure(width=150)
btnPesquisarHisto.pack(side="left", padx=5)

TabelaLivroHisto = ttk.Treeview(
    histFrame,
    columns=("ID", "LIVRO", "ID_Vendedor", "PRECO_UNIT", "TOTAL", "DATA", "STATUS"),
    show="tree headings"
)

TabelaLivroHisto.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

TabelaLivroHisto.heading("ID", text="ID DA VENDA")
TabelaLivroHisto.heading("LIVRO", text="LIVROS")
TabelaLivroHisto.heading("ID_Vendedor", text="ID DO VENDEDOR")
TabelaLivroHisto.heading("PRECO_UNIT", text="PREÇO UNITÁRIO")
TabelaLivroHisto.heading("TOTAL", text="TOTAL DA VENDA")
TabelaLivroHisto.heading("DATA", text="DATA")
TabelaLivroHisto.heading("STATUS", text="STATUS")

TabelaLivroHisto.column("#0", width=30, stretch=False)
TabelaLivroHisto.column("ID", width=90)
TabelaLivroHisto.column("LIVRO", width=300)
TabelaLivroHisto.column("ID_Vendedor", width=130)
TabelaLivroHisto.column("PRECO_UNIT", width=120)
TabelaLivroHisto.column("TOTAL", width=120)
TabelaLivroHisto.column("DATA", width=150)
TabelaLivroHisto.column("STATUS", width=100)

# vendas canceladas aparecem em vermelho
TabelaLivroHisto.tag_configure("cancelada", foreground="#B91C1C")

criar_botao(
    histFrame,
    "Cancelar venda",
    CancelarVendaHisto
).pack(pady=8)

criar_botao(
    histFrame,
    "Voltar",
    voltar
).pack(pady=8)

# ==========================================
# FRAME DE CADASTRO DE USUARIO
# ==========================================
AddUser = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    AddUser,
    "Cadastrar usuario"
).pack(pady=20)

ctk.CTkLabel(AddUser, text="Nome do usúario", text_color=LETRAS).pack()
UserAdd = criar_campo(AddUser)
UserAdd.pack(pady=5)

ctk.CTkLabel(AddUser, text="Senha do usuario", text_color=LETRAS).pack()
SenhaAdd = criar_campo(AddUser)
SenhaAdd.pack(pady=5)

ctk.CTkLabel(AddUser, text="Tipo do usuario", text_color=LETRAS).pack()

TipoAdd = ctk.StringVar(value="Funcionario")

for tipo in ("Admin", "Gerente", "Funcionario"):

    ctk.CTkRadioButton(
        AddUser,
        text=tipo,
        variable=TipoAdd,
        value=tipo,
        text_color=LETRAS,
        fg_color=LETRAS,
        border_color=LETRAS
    ).pack(pady=4)

criar_botao(
    AddUser,
    "Adicionar",
    addUser
).pack(pady=8)

criar_botao(
    AddUser,
    "Voltar",
    voltar
).pack(pady=8)


# ==========================================
# LISTA DE TELAS
# ==========================================

todas_telas = [
    loginFrame,
    main,
    Addframe,
    delFrame,
    BuscFrame,
    VendaFrame,
    UpdFrame,
    histFrame,
    AddUser
]


# ==========================================
# INICIAR PROGRAMA
# ==========================================

tipo_usuario = None
usuario_logado = None


janela.mainloop()

