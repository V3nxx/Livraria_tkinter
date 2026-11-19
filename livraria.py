import re
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from validacao import (
    adicionar_Livro,
    deletar_livro,
    Buscar_Livro,
    Atualizar_livro,
    verificar_login,
    Verificar_Tipo_Login,
    Buscar_Livro_venda,
    Finalizar_Venda,
    Buscar_Historico,
    Cancelar_Venda,
    adicionar_usuario,
    listar_usuarios,
    atualizar_usuario,
    remover_usuario,
    existe_admin
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

# ==========================================
# PERMISSÕES (o que cada tipo de usuário pode acessar)
# ==========================================

PERMISSOES = {
    "Admin": ("Cadastrar", "Deletar", "Buscar", "Atualizar", "Historico", "Venda", "Usuarios"),
    "Gerente": ("Cadastrar", "Deletar", "Buscar", "Atualizar", "Historico"),
    "Funcionario": ("Buscar", "Venda"),
}


def pode(acao):

    return acao in PERMISSOES.get(tipo_usuario, ())


# ESC para sair do fullscreen
janela.bind(
    "<Escape>",
    lambda event: janela.attributes("-fullscreen", False)
)


# ==========================================
# VALIDAÇÃO DOS CAMPOS NUMÉRICOS
# (o campo simplesmente não aceita letras nem símbolos)
# ==========================================

def _valida_preco(texto):

    # ate 7 digitos, e opcionalmente "." ou "," com ate 2 casas
    return re.fullmatch(r"[0-9]{0,7}([.,][0-9]{0,2})?", texto) is not None


def _valida_inteiro(texto):

    return re.fullmatch(r"[0-9]{0,7}", texto) is not None


VALIDA_PRECO = (janela.register(_valida_preco), "%P")
VALIDA_INTEIRO = (janela.register(_valida_inteiro), "%P")


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


# tipo: None (texto livre), "preco" ou "inteiro" (so aceitam numeros)
# Campos numericos nao usam placeholder (o texto de exemplo seria barrado pela validacao)

def criar_campo(frame, placeholder="", tipo=None):

    extras = {}

    if tipo == "preco":
        extras = {"validate": "key", "validatecommand": VALIDA_PRECO}
    elif tipo == "inteiro":
        extras = {"validate": "key", "validatecommand": VALIDA_INTEIRO}

    return ctk.CTkEntry(
        frame,
        width=250,
        height=40,
        placeholder_text=placeholder,
        fg_color=BOTAO,
        text_color=LETRAS,
        border_color=LETRAS,
        corner_radius=8,
        **extras
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
    aviso.geometry("460x260")
    aviso.configure(fg_color=FUNDO)
    aviso.attributes("-topmost", True)

    ctk.CTkLabel(
        aviso,
        text=texto,
        text_color=LETRAS,
        font=("Arial", 14),
        wraplength=410
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

    # o campo de usuario fica travado ao editar; precisa destravar para limpar
    UserAdd.configure(state="normal")

    # apaga tudo que foi digitado/listado, para nada ficar salvo ao trocar de tela
    campos = [
        Usuario, Senha,
        SetupUser, SetupSenha, SetupConfirma,
        TituloAdd, AutorAdd, CategAdd, PrecoAdd, QuantAdd,
        LivroDel,
        barraBusca,
        idVenda, qtdVenda,
        TituloUpd, AutorUpd, CategUpd, PrecoUpd, QuantUpd, IdUpd,
        idVendaHisto, dataHisto, vendedorHisto,
        UserAdd, SenhaAdd
    ]

    for campo in campos:
        campo.delete(0, "end")

    qtdVenda.insert(0, "1")

    TipoAdd.set("Funcionario")

    for tabela in (TabelaLivro, TabelaLivroHisto, TabelaUser):
        for item in tabela.get_children():
            tabela.delete(item)

    limpar_venda()

    loginErro.configure(text="")
    setupErro.configure(text="")

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

    if not pode("Historico"):
        return

    esconder_telas()
    PesquisarHisto()
    histFrame.pack(fill="both", expand=True)


def menuAdd():

    if not pode("Cadastrar"):
        return

    esconder_telas()
    Addframe.pack(fill="both", expand=True)


def menuDel():

    if not pode("Deletar"):
        return

    esconder_telas()
    delFrame.pack(fill="both", expand=True)


def menuBusc():

    if not pode("Buscar"):
        return

    esconder_telas()
    BuscFrame.pack(fill="both", expand=True)


def menuUpd():

    if not pode("Atualizar"):
        return

    esconder_telas()
    UpdFrame.pack(fill="both", expand=True)


def menuVenda():

    if not pode("Venda"):
        return

    esconder_telas()
    VendaFrame.pack(fill="both", expand=True)


def menuUser():

    if not pode("Usuarios"):
        return

    esconder_telas()
    listarUsuariosTela()
    UsersFrame.pack(fill="both", expand=True)


# Mostra a primeira tela do programa: se nao existe nenhum Admin no banco,
# pede para criar um; senao mostra o login

def mostrar_inicio():

    esconder_telas()

    if existe_admin():
        loginFrame.pack(fill="both", expand=True)
    else:
        SetupFrame.pack(fill="both", expand=True)


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

    todos = [
        ("Cadastrar", "Cadastrar", menuAdd),
        ("Deletar", "Deletar", menuDel),
        ("Buscar", "Buscar", menuBusc),
        ("Atualizar Cadastro", "Atualizar", menuUpd),
        ("Venda", "Venda", menuVenda),
        ("Historico de vendas", "Historico", menuHist),
        ("Usuarios", "Usuarios", menuUser)
    ]

    botoes = [(texto, comando) for texto, acao, comando in todos if pode(acao)]

    if not botoes:
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
# PRIMEIRO ACESSO (CRIAR ADMINISTRADOR)
# ==========================================

def criarAdmin():

    usuario = SetupUser.get().strip()
    senha = SetupSenha.get()
    confirma = SetupConfirma.get()

    if senha != confirma:
        setupErro.configure(text="As senhas não coincidem.")
        return

    ok, msg = adicionar_usuario(usuario, senha, "Admin")

    if not ok:
        setupErro.configure(text=msg)
        return

    mostrar_inicio()
    mostrar_aviso("Conta de administrador criada!\nFaça login para continuar.")


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

    global tipo_usuario, usuario_logado

    tipo_usuario = None
    usuario_logado = None

    # mostrar_inicio limpa campos, tabelas e carrinho para o proximo usuario nao ver nada
    mostrar_inicio()


# ==========================================
# CADASTRAR LIVRO
# ==========================================

def addLivro():

    ok, msg = adicionar_Livro(
        TituloAdd.get(),
        AutorAdd.get(),
        CategAdd.get(),
        PrecoAdd.get(),
        QuantAdd.get()
    )

    if ok:
        voltar()
    else:
        mostrar_aviso(msg)


# ==========================================
# ATUALIZAR LIVRO
# ==========================================

def updLivro():

    ok, msg = Atualizar_livro(
        TituloUpd.get(),
        AutorUpd.get(),
        CategUpd.get(),
        PrecoUpd.get(),
        QuantUpd.get(),
        IdUpd.get()
    )

    if ok:
        voltar()
    else:
        mostrar_aviso(msg)


# ==========================================
# DELETAR LIVRO
# ==========================================

def delLivro():

    ok, msg = deletar_livro(LivroDel.get())

    if ok:
        voltar()
    else:
        mostrar_aviso(msg)


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
# VENDAS (CARRINHO)
# ==========================================

# livro_id -> {"titulo", "autor", "categoria", "preco", "qtd"}
carrinho = {}


def atualizar_carrinho():

    for item in TabelaLivroVenda.get_children():
        TabelaLivroVenda.delete(item)

    total = 0.0

    for livro_id, item in carrinho.items():

        subtotal = item["preco"] * item["qtd"]
        total += subtotal

        TabelaLivroVenda.insert(
            "",
            tk.END,
            iid=str(livro_id),
            values=(
                livro_id,
                item["titulo"],
                item["autor"],
                item["categoria"],
                f"{item['preco']:.2f}",
                item["qtd"],
                f"{subtotal:.2f}"
            )
        )

    ValorTotal.configure(
        text=f"Total: R$ {total:.2f}"
    )


def limpar_venda():

    carrinho.clear()
    atualizar_carrinho()


def AdicionarCarrinho():

    texto_id = idVenda.get().strip()
    texto_qtd = qtdVenda.get().strip()

    if not texto_id:
        mostrar_aviso("Digite o ID do livro.")
        return

    if not texto_qtd or int(texto_qtd) < 1:
        mostrar_aviso("Digite uma quantidade maior que zero.")
        return

    livro_id = int(texto_id)
    qtd = int(texto_qtd)

    livro = Buscar_Livro_venda(livro_id)

    if not livro:
        mostrar_aviso("Livro não encontrado. Confira o ID.")
        return

    estoque = _para_int(livro[5])
    ja_no_carrinho = carrinho[livro_id]["qtd"] if livro_id in carrinho else 0

    if ja_no_carrinho + qtd > estoque:
        mostrar_aviso(
            f"Estoque insuficiente de '{livro[1]}'.\n"
            f"Em estoque: {estoque}  |  Já no carrinho: {ja_no_carrinho}"
        )
        return

    # mesmo livro de novo = soma na linha que ja existe
    if livro_id in carrinho:
        carrinho[livro_id]["qtd"] += qtd
    else:
        carrinho[livro_id] = {
            "titulo": livro[1],
            "autor": livro[2],
            "categoria": livro[3],
            "preco": _para_float(livro[4]),
            "qtd": qtd
        }

    atualizar_carrinho()

    idVenda.delete(0, "end")
    qtdVenda.delete(0, "end")
    qtdVenda.insert(0, "1")
    idVenda.focus()


def RemoverDoCarrinho():

    selecao = TabelaLivroVenda.selection()

    if not selecao:
        mostrar_aviso("Selecione um livro do carrinho para remover.")
        return

    for iid in selecao:
        carrinho.pop(int(iid), None)

    atualizar_carrinho()


def FinalizarVenda():

    if not carrinho:
        mostrar_aviso("O carrinho está vazio.")
        return

    itens = [(livro_id, item["qtd"]) for livro_id, item in carrinho.items()]

    ok, resultado = Finalizar_Venda(itens, usuario_logado)

    if ok:

        compra_id, total = resultado

        limpar_venda()

        mostrar_aviso(f"Venda {compra_id} concluída!\nTotal: R$ {total:.2f}")

    else:

        # nada foi vendido; o carrinho continua para o funcionario ajustar
        mostrar_aviso(
            "Venda não realizada. Sem estoque suficiente:\n\n"
            + "\n".join(resultado)
        )


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

        quantidade_total = sum(qtd for _, qtd, _ in livros)

        # linha principal = a venda (com o valor total)
        pai = TabelaLivroHisto.insert(
            "",
            tk.END,
            values=(compra_id, f"{quantidade_total} livro(s)", vendedor_id, "", total, data_venda, status),
            open=True,
            tags=tags
        )

        # linhas de baixo = cada livro da venda (com quantidade e preco unitario)
        for titulo, qtd, preco in livros:

            TabelaLivroHisto.insert(
                pai,
                tk.END,
                values=("", f"{titulo}  (x{qtd})", "", preco, "", "", ""),
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
# USUÁRIOS (LISTAR / ADICIONAR / EDITAR / REMOVER)
# ==========================================

# None = formulario esta cadastrando; senao guarda o usuario que esta sendo editado
usuario_editando = None


def listarUsuariosTela():

    for item in TabelaUser.get_children():
        TabelaUser.delete(item)

    for usuario, tipo in listar_usuarios():

        # o nome do usuario e o iid da linha (assim nunca perde zeros a esquerda etc.)
        TabelaUser.insert(
            "",
            tk.END,
            iid=usuario,
            values=(usuario, tipo)
        )


def usuario_selecionado():

    selecao = TabelaUser.selection()

    if not selecao:
        mostrar_aviso("Selecione um usuário na lista.")
        return None

    return str(selecao[0])


def novoUsuario():

    global usuario_editando

    esconder_telas()

    usuario_editando = None

    TituloUserForm.configure(text="Novo usuário")
    dicaSenha.configure(text="")

    AddUser.pack(fill="both", expand=True)


def editarUsuario():

    global usuario_editando

    usuario = usuario_selecionado()

    if usuario is None:
        return

    tipo = TabelaUser.item(usuario, "values")[1]

    esconder_telas()

    usuario_editando = usuario

    TituloUserForm.configure(text="Editar usuário")
    dicaSenha.configure(text="Deixe a senha em branco para manter a atual.")

    UserAdd.insert(0, usuario)
    UserAdd.configure(state="disabled")   # o nome do usuario nao muda
    TipoAdd.set(str(tipo))

    AddUser.pack(fill="both", expand=True)


def salvarUsuario():

    global tipo_usuario

    senha = SenhaAdd.get()
    tipo = TipoAdd.get()

    if usuario_editando is None:
        ok, msg = adicionar_usuario(UserAdd.get(), senha, tipo)
    else:
        ok, msg = atualizar_usuario(usuario_editando, senha, tipo)

    if not ok:
        mostrar_aviso(msg)
        return

    # se mudou o proprio tipo, atualiza o menu da sessao atual
    if usuario_editando is not None and usuario_editando == usuario_logado:

        tipo_usuario = tipo
        criar_menu()

        if not pode("Usuarios"):
            voltar()
            return

    menuUser()


def removerUsuarioTela():

    usuario = usuario_selecionado()

    if usuario is None:
        return

    confirmar = messagebox.askyesno(
        "Remover usuário",
        f"Remover o usuário '{usuario}'?"
    )

    if not confirmar:
        return

    ok, msg = remover_usuario(usuario, usuario_logado)

    if ok:
        listarUsuariosTela()
    else:
        mostrar_aviso(msg)


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
# FRAME DE PRIMEIRO ACESSO (CRIAR ADMINISTRADOR)
# ==========================================

SetupFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

setupCentro = ctk.CTkFrame(
    SetupFrame,
    fg_color="transparent"
)

setupCentro.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

criar_titulo(
    setupCentro,
    "Primeiro acesso"
).pack(pady=20)

ctk.CTkLabel(
    setupCentro,
    text="Nenhuma conta de administrador foi encontrada.\nCrie uma para continuar.",
    text_color=LETRAS,
    font=("Arial", 16),
    justify="center"
).pack(pady=10)

SetupUser = criar_campo(
    setupCentro,
    "Usuário"
)
SetupUser.pack(pady=8)

SetupSenha = criar_campo(
    setupCentro,
    "Senha"
)
SetupSenha.configure(show="*")
SetupSenha.pack(pady=8)

SetupConfirma = criar_campo(
    setupCentro,
    "Confirmar senha"
)
SetupConfirma.configure(show="*")
SetupConfirma.pack(pady=8)

criar_botao(
    setupCentro,
    "Criar administrador",
    criarAdmin
).pack(pady=15)

setupErro = ctk.CTkLabel(
    setupCentro,
    text="",
    text_color="#B91C1C",
    wraplength=300
)
setupErro.pack()


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

ctk.CTkLabel(Addframe, text="Preço (ex: 29.90):", text_color=LETRAS).pack()
PrecoAdd = criar_campo(Addframe, tipo="preco")
PrecoAdd.pack(pady=5)

ctk.CTkLabel(Addframe, text="Quantidade:", text_color=LETRAS).pack()
QuantAdd = criar_campo(Addframe, tipo="inteiro")
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
    text="ID do livro:",
    text_color=LETRAS
).pack()

LivroDel = criar_campo(delFrame, tipo="inteiro")
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
).pack(pady=15)

# linha: ID do livro + quantidade + botao de adicionar
linhaAdd = ctk.CTkFrame(
    VendaFrame,
    fg_color="transparent"
)
linhaAdd.pack(pady=5)

colunaId = ctk.CTkFrame(linhaAdd, fg_color="transparent")
colunaId.pack(side="left", padx=8)

ctk.CTkLabel(colunaId, text="ID do livro:", text_color=LETRAS).pack()
idVenda = criar_campo(colunaId, tipo="inteiro")
idVenda.configure(width=180)
idVenda.pack()

colunaQtd = ctk.CTkFrame(linhaAdd, fg_color="transparent")
colunaQtd.pack(side="left", padx=8)

ctk.CTkLabel(colunaQtd, text="Quantidade:", text_color=LETRAS).pack()
qtdVenda = criar_campo(colunaQtd, tipo="inteiro")
qtdVenda.configure(width=120)
qtdVenda.pack()

criar_botao(
    linhaAdd,
    "Adicionar ao carrinho",
    AdicionarCarrinho
).pack(side="left", padx=8, anchor="s")

# Enter tambem adiciona ao carrinho
idVenda.bind("<Return>", lambda event: AdicionarCarrinho())
qtdVenda.bind("<Return>", lambda event: AdicionarCarrinho())

ValorTotal = ctk.CTkLabel(
    VendaFrame,
    text="Total: R$ 0.00",
    text_color=LETRAS,
    font=("Arial", 18, "bold")
)
ValorTotal.pack(pady=8)

linhaBotoes = ctk.CTkFrame(
    VendaFrame,
    fg_color="transparent"
)
linhaBotoes.pack(pady=5)

criar_botao(
    linhaBotoes,
    "Finalizar venda",
    FinalizarVenda
).pack(side="left", padx=6)

criar_botao(
    linhaBotoes,
    "Remover selecionado",
    RemoverDoCarrinho
).pack(side="left", padx=6)

criar_botao(
    linhaBotoes,
    "Limpar carrinho",
    limpar_venda
).pack(side="left", padx=6)

# o botao Voltar e empacotado antes da tabela para nunca ficar sem espaco
criar_botao(
    VendaFrame,
    "Voltar",
    voltar
).pack(side="bottom", pady=8)

TabelaLivroVenda = ttk.Treeview(
    VendaFrame,
    columns=("ID", "TITULO", "AUTOR", "CATEGORIA", "PREÇO", "QTD", "SUBTOTAL"),
    show="headings",
    selectmode="browse"
)

TabelaLivroVenda.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

for coluna in ("ID", "TITULO", "AUTOR", "CATEGORIA", "PREÇO", "QTD", "SUBTOTAL"):
    TabelaLivroVenda.heading(coluna, text=coluna)

TabelaLivroVenda.column("ID", width=50)
TabelaLivroVenda.column("TITULO", width=200)
TabelaLivroVenda.column("AUTOR", width=150)
TabelaLivroVenda.column("CATEGORIA", width=120)
TabelaLivroVenda.column("PREÇO", width=100)
TabelaLivroVenda.column("QTD", width=70)
TabelaLivroVenda.column("SUBTOTAL", width=100)


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
PrecoUpd = criar_campo(UpdFrame, tipo="preco")
PrecoUpd.pack(pady=5)

ctk.CTkLabel(UpdFrame, text="Quantidade:", text_color=LETRAS).pack()
QuantUpd = criar_campo(UpdFrame, tipo="inteiro")
QuantUpd.pack(pady=5)

ctk.CTkLabel(UpdFrame, text="ID:", text_color=LETRAS).pack()
IdUpd = criar_campo(UpdFrame, tipo="inteiro")
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
# FRAME DA LISTA DE USUARIOS
# ==========================================

UsersFrame = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

criar_titulo(
    UsersFrame,
    "Usuários"
).pack(pady=25)

linhaBotoesUser = ctk.CTkFrame(
    UsersFrame,
    fg_color="transparent"
)
linhaBotoesUser.pack(pady=5)

criar_botao(
    linhaBotoesUser,
    "Novo usuário",
    novoUsuario
).pack(side="left", padx=6)

criar_botao(
    linhaBotoesUser,
    "Editar selecionado",
    editarUsuario
).pack(side="left", padx=6)

criar_botao(
    linhaBotoesUser,
    "Remover selecionado",
    removerUsuarioTela
).pack(side="left", padx=6)

criar_botao(
    UsersFrame,
    "Voltar",
    voltar
).pack(side="bottom", pady=8)

TabelaUser = ttk.Treeview(
    UsersFrame,
    columns=("USUARIO", "TIPO"),
    show="headings",
    selectmode="browse"
)

TabelaUser.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

TabelaUser.heading("USUARIO", text="USUÁRIO")
TabelaUser.heading("TIPO", text="TIPO")

TabelaUser.column("USUARIO", width=250)
TabelaUser.column("TIPO", width=150)


# ==========================================
# FRAME DO FORMULARIO DE USUARIO (NOVO / EDITAR)
# ==========================================

AddUser = ctk.CTkFrame(
    janela,
    fg_color=FUNDO
)

TituloUserForm = criar_titulo(
    AddUser,
    "Novo usuário"
)
TituloUserForm.pack(pady=20)

ctk.CTkLabel(AddUser, text="Nome do usuário", text_color=LETRAS).pack()
UserAdd = criar_campo(AddUser)
UserAdd.pack(pady=5)

ctk.CTkLabel(AddUser, text="Senha do usuário", text_color=LETRAS).pack()
SenhaAdd = criar_campo(AddUser)
SenhaAdd.configure(show="*")
SenhaAdd.pack(pady=5)

dicaSenha = ctk.CTkLabel(
    AddUser,
    text="",
    text_color=LETRAS,
    font=("Arial", 12)
)
dicaSenha.pack()

ctk.CTkLabel(AddUser, text="Tipo do usuário", text_color=LETRAS).pack()

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
    "Salvar",
    salvarUsuario
).pack(pady=8)

criar_botao(
    AddUser,
    "Cancelar",
    menuUser
).pack(pady=8)


# ==========================================
# LISTA DE TELAS
# ==========================================

todas_telas = [
    loginFrame,
    SetupFrame,
    main,
    Addframe,
    delFrame,
    BuscFrame,
    VendaFrame,
    UpdFrame,
    histFrame,
    UsersFrame,
    AddUser
]


# ==========================================
# INICIAR PROGRAMA
# ==========================================

tipo_usuario = None
usuario_logado = None

# sem nenhum Admin no banco abre a tela de criar administrador; senao, o login
mostrar_inicio()

janela.mainloop()
