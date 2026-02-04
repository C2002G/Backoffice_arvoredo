import flet as ft
from database import *
from datetime import datetime

# ===== CONFIGURAÇÕES GLOBAIS =====
COR_PRIMARIA = "#2d8f4c"  # Verde Arvoredo
COR_PRIMARIA_ESCURA = "#1f6336"
COR_SECUNDARIA = "#f5f5f5"

# ===== VARIÁVEIS GLOBAIS =====
tela_atual = "cadastro"


def criar_header(page, mudar_tela_fn):
    """Cria o header fixo com abas de navegação"""
    botoes = {
        "📦 Cadastrar": "cadastro",
        "✏️ Editar": "editar",
        "📊 Vendas": "vendas",
        "👥 Clientes": "clientes",
        "📋 Pedidos": "pedidos",
    }

    botoes_row = ft.Row(
        [
            ft.ElevatedButton(
                nome,
                on_click=lambda e, t=tab: mudar_tela_fn(t),
                color=ft.Colors.WHITE,
                bgcolor=COR_PRIMARIA,
                width=140,
                height=50,
            )
            for nome, tab in botoes.items()
        ],
        spacing=10,
        wrap=True,
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "🌳 ARVOREDO - Sistema de Estoque",
                            size=24,
                            weight="bold",
                            color=ft.Colors.WHITE,
                        ),
                    ]
                ),
                botoes_row,
            ],
            spacing=10,
        ),
        bgcolor=COR_PRIMARIA_ESCURA,
        padding=15,
        border_radius=10,
    )

    return header


# ===== TELA 1: CADASTRAR PRODUTOS =====    
def criar_tela_cadastro(page, atualizar_fn):
    """Tela para cadastrar novos produtos e suas marcas"""

    nome_prod = ft.TextField(label="Nome do Produto", width=300)
    categoria_dd = ft.Dropdown(
        label="Categoria",
        width=200,
        options=[
            ft.dropdown.Option("Mercado"),
            ft.dropdown.Option("Lancheria"),
            ft.dropdown.Option("Bebidas"),
            ft.dropdown.Option("Alimentos"),
        ],
    )

    codigo_marca = ft.TextField(label="Código", width=150)
    marca_nome = ft.TextField(label="Marca", width=150)
    preco_un = ft.TextField(label="Preço Unitário", width=150, keyboard_type="number")
    qtd_marca = ft.TextField(
        label="Quantidade", width=150, keyboard_type="number", value="0"
    )

    msg_status = ft.Text("", color=ft.Colors.RED)

    def cadastrar(e):
        if not nome_prod.value or not categoria_dd.value or not marca_nome.value:
            msg_status.value = "❌ Preencha todos os campos!"
            msg_status.color = ft.Colors.RED
            page.update()
            return

        # Inserir produto
        sucesso, msg, prod_id = inserir_produto(nome_prod.value, categoria_dd.value)
        if not sucesso:
            msg_status.value = f"❌ {msg}"
            msg_status.color = ft.Colors.RED
            page.update()
            return

        # Inserir marca do produto
        sucesso2, msg2, marca_id = inserir_marca_produto(
            prod_id,
            codigo_marca.value or f"PROD{prod_id}",
            marca_nome.value,
            float(preco_un.value or 0),
        )

        if sucesso2 and marca_id != -1:
            # Atualizar quantidade
            atualizar_quantidade_marca(marca_id, int(qtd_marca.value or 0))
            msg_status.value = (
                f"✅ Produto cadastrado: {nome_prod.value} - {marca_nome.value}"
            )
            msg_status.color = ft.Colors.GREEN

            # Limpar campos
            nome_prod.value = ""
            categoria_dd.value = ""
            marca_nome.value = ""
            preco_un.value = ""
            qtd_marca.value = "0"
            codigo_marca.value = ""

            atualizar_fn()
        else:
            msg_status.value = f"❌ {msg2}"
            msg_status.color = ft.Colors.RED

        page.update()

    # Listar produtos
    produtos_list = ft.ListView(spacing=10, expand=True)

    def atualizar_lista():
        produtos_list.controls.clear()
        produtos = listar_produtos()
        for prod in produtos:
            marcas = listar_marcas_produto(prod["id"])
            marcas_texto = ", ".join(
                [f"{m['marca']} ({m['quantidade']})" for m in marcas]
            )

            produtos_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(f"{prod['nome']}", weight="bold", size=14),
                                    ft.Text(
                                        f"Categoria: {prod['categoria']}",
                                        size=11,
                                        color=ft.Colors.GREY_700,
                                    ),
                                    ft.Text(
                                        f"Marcas: {marcas_texto}",
                                        size=11,
                                        color=ft.Colors.GREY_700,
                                    ),
                                    ft.Text(
                                        f"Total: {prod['quantidade_total'] or 0} un | Valor: R$ {prod['valor_total'] or 0:.2f}",
                                        weight="bold",
                                        color=COR_PRIMARIA,
                                    ),
                                ],
                                spacing=5,
                                expand=True,
                            ),
                            ft.ElevatedButton("✏️ Editar", width=80, height=40),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                )
            )
        page.update()

    # Primeira atualização
    atualizar_lista()

    tela = ft.Column(
        [
            ft.Text(
                "📦 Cadastrar Produtos", size=22, weight="bold", color=COR_PRIMARIA
            ),
            ft.Divider(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Adicionar Novo Produto", size=18, weight="bold"),
                            ft.Row([nome_prod, categoria_dd], wrap=True),
                            ft.Row(
                                [codigo_marca, marca_nome, preco_un, qtd_marca],
                                wrap=True,
                            ),
                            ft.ElevatedButton(
                                "➕ Cadastrar Produto",
                                on_click=cadastrar,
                                color=ft.Colors.WHITE,
                                bgcolor=COR_PRIMARIA,
                                width=300,
                                height=50,
                            ),
                            msg_status,
                        ],
                        spacing=10,
                    ),
                    padding=20,
                )
            ),
            ft.Divider(),
            ft.Text("Produtos Cadastrados", size=18, weight="bold", color=COR_PRIMARIA),
            ft.Container(content=produtos_list, expand=True, height=400),
        ],
        spacing=15,
        expand=True,
        scroll="auto",
    )

    # Retornar função de atualização
    tela.atualizar = atualizar_lista
    return tela


# ===== TELA 2: EDITAR PRODUTOS =====
def criar_tela_editar(page):
    """Tela para editar produtos e ver histórico"""

    busca = ft.TextField(label="🔍 Buscar produto...", width=400)
    resultado_lista = ft.ListView(spacing=10, expand=True)

    def buscar_produtos(e):
        resultado_lista.controls.clear()
        termo = busca.value.lower()
        produtos = listar_produtos()

        for prod in produtos:
            if termo in prod["nome"].lower() or not termo:
                marcas = listar_marcas_produto(prod["id"])

                def criar_cards_marcas(prod_id, marcas_list):
                    col = ft.Column(spacing=5)
                    for marca in marcas_list:
                        historico = listar_historico_marca(marca["id"])
                        hist_texto = f"\n".join(
                            [
                                f"  • {h['tipo']}: {h['quantidade']} un - {h['data_hora']}"
                                for h in historico[-3:]
                            ]
                        )

                        col.controls.append(
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Column(
                                                    [
                                                        ft.Text(
                                                            f"  {marca['marca']} | Código: {marca['codigo']}",
                                                            weight="bold",
                                                        ),
                                                        ft.Text(
                                                            f"  Preço: R$ {marca['preco_unitario']:.2f} | Estoque: {marca['quantidade']} un",
                                                            color=ft.Colors.GREY_700,
                                                        ),
                                                    ]
                                                ),
                                                ft.ElevatedButton(
                                                    "✏️", width=40, height=40
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        (
                                            ft.Text(
                                                "Histórico:", size=10, weight="bold"
                                            )
                                            if historico
                                            else None
                                        ),
                                        (
                                            ft.Text(
                                                hist_texto,
                                                size=9,
                                                color=ft.Colors.GREY_700,
                                            )
                                            if historico
                                            else None
                                        ),
                                    ],
                                    spacing=3,
                                ),
                                padding=10,
                                bgcolor=ft.Colors.GREY_100,
                                border_radius=5,
                            )
                        )
                    return col

                resultado_lista.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    f"{prod['nome']} (Total: {prod['quantidade_total'] or 0} un)",
                                    weight="bold",
                                    size=14,
                                    color=COR_PRIMARIA,
                                ),
                                ft.Text(
                                    f"Categoria: {prod['categoria']}",
                                    size=11,
                                    color=ft.Colors.GREY_700,
                                ),
                                criar_cards_marcas(prod["id"], marcas),
                            ],
                            spacing=5,
                        ),
                        border=ft.border.all(1, COR_PRIMARIA),
                        border_radius=8,
                        padding=12,
                        bgcolor=ft.Colors.WHITE,
                    )
                )

        page.update()

    busca.on_change = buscar_produtos
    buscar_produtos(None)

    tela = ft.Column(
        [
            ft.Text("✏️ Editar Produtos", size=22, weight="bold", color=COR_PRIMARIA),
            ft.Divider(),
            busca,
            ft.Container(content=resultado_lista, expand=True, height=500),
        ],
        spacing=15,
        expand=True,
        scroll="auto",
    )

    return tela


# ===== TELA 3: REGISTRO DE VENDAS =====
def criar_tela_vendas(page):
    """Tela para visualizar histórico de vendas"""

    vendas_lista = ft.ListView(spacing=10, expand=True)

    def atualizar_vendas():
        vendas_lista.controls.clear()
        vendas = listar_vendas()

        if not vendas:
            vendas_lista.controls.append(
                ft.Text("Nenhuma venda registrada", color=ft.Colors.GREY_700)
            )
        else:
            for venda in vendas:
                vendas_lista.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            f"{venda['nome']} - {venda['marca']}",
                                            weight="bold",
                                        ),
                                        ft.Text(
                                            f"Cliente: {venda['cliente']}",
                                            size=11,
                                            color=ft.Colors.GREY_700,
                                        ),
                                        ft.Text(
                                            f"Entrada: {venda['data_cadastro']} | Quantidade: {venda['quantidade']} un",
                                            size=10,
                                            color=ft.Colors.GREY_700,
                                        ),
                                        ft.Text(
                                            f"Subtotal: R$ {venda['subtotal']:.2f}",
                                            weight="bold",
                                            color=COR_PRIMARIA,
                                        ),
                                    ],
                                    spacing=3,
                                    expand=True,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=8,
                        padding=10,
                        bgcolor=ft.Colors.WHITE,
                    )
                )

        page.update()

    atualizar_vendas()

    tela = ft.Column(
        [
            ft.Text(
                "📊 Registro de Vendas", size=22, weight="bold", color=COR_PRIMARIA
            ),
            ft.Divider(),
            ft.Container(content=vendas_lista, expand=True, height=500),
        ],
        spacing=15,
        expand=True,
        scroll="auto",
    )

    return tela


# ===== TELA 4: CLIENTES/FIADOS =====
def criar_tela_clientes(page):
    """Tela para gerenciar clientes e fiados"""

    nome_cli = ft.TextField(label="Nome do Cliente", width=250)
    apelido_cli = ft.TextField(label="Apelido", width=200)
    cpf_cli = ft.TextField(label="CPF (opcional)", width=200, keyboard_type="number")
    fiando_check = ft.Checkbox(label="Cliente de fiado", value=False)

    msg_status = ft.Text("", color=ft.Colors.RED)
    clientes_lista = ft.ListView(spacing=10, expand=True)

    def cadastrar_cliente(e):
        if not nome_cli.value:
            msg_status.value = "❌ Digite o nome do cliente!"
            msg_status.color = ft.Colors.RED
            page.update()
            return

        sucesso, msg, _ = inserir_cliente(
            nome_cli.value, apelido_cli.value, cpf_cli.value, fiando_check.value
        )

        if sucesso:
            msg_status.value = f"✅ Cliente cadastrado: {nome_cli.value}"
            msg_status.color = ft.Colors.GREEN
            nome_cli.value = ""
            apelido_cli.value = ""
            cpf_cli.value = ""
            fiando_check.value = False
            atualizar_clientes()
        else:
            msg_status.value = f"❌ {msg}"
            msg_status.color = ft.Colors.RED

        page.update()

    def atualizar_clientes():
        clientes_lista.controls.clear()
        clientes = listar_clientes()

        for cliente in clientes:
            pedidos = listar_pedidos_cliente(cliente["id"])
            fiado_tag = "🔴 FIADO" if cliente["fiando"] else "✅ Pago"

            clientes_lista.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        f"{cliente['nome']}", weight="bold", size=14
                                    ),
                                    ft.Text(
                                        f"Apelido: {cliente['apelido'] or '-'} | CPF: {cliente['cpf'] or '-'}",
                                        size=10,
                                        color=ft.Colors.GREY_700,
                                    ),
                                    ft.Text(
                                        f"Pedidos: {len(pedidos)} | Status: {fiado_tag}",
                                        size=10,
                                        weight="bold",
                                        color=(
                                            COR_PRIMARIA
                                            if cliente["fiando"]
                                            else ft.Colors.GREEN
                                        ),
                                    ),
                                ],
                                spacing=3,
                                expand=True,
                            ),
                            ft.ElevatedButton("Ver Pedidos", width=100, height=40),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=10,
                    bgcolor=ft.Colors.WHITE,
                )
            )

        page.update()

    atualizar_clientes()

    tela = ft.Column(
        [
            ft.Text("👥 Clientes / Fiados", size=22, weight="bold", color=COR_PRIMARIA),
            ft.Divider(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Adicionar Novo Cliente", size=18, weight="bold"),
                            ft.Row([nome_cli, apelido_cli, cpf_cli], wrap=True),
                            fiando_check,
                            ft.ElevatedButton(
                                "➕ Cadastrar Cliente",
                                on_click=cadastrar_cliente,
                                color=ft.Colors.WHITE,
                                bgcolor=COR_PRIMARIA,
                                width=300,
                                height=50,
                            ),
                            msg_status,
                        ],
                        spacing=10,
                    ),
                    padding=20,
                )
            ),
            ft.Divider(),
            ft.Text("Clientes Cadastrados", size=18, weight="bold", color=COR_PRIMARIA),
            ft.Container(content=clientes_lista, expand=True, height=400),
        ],
        spacing=15,
        expand=True,
        scroll="auto",
    )

    return tela


# ===== TELA 5: REGISTRAR PEDIDOS =====
def criar_tela_pedidos(page):
    """Tela para criar pedidos (similar ao oncomandas)"""

    clientes_lista_dd = ft.Dropdown(label="Cliente", width=300)

    def atualizar_clientes_dd(e=None):
        clientes_lista_dd.options.clear()
        for cliente in listar_clientes():
            clientes_lista_dd.options.append(
                ft.dropdown.Option(str(cliente["id"]), cliente["nome"])
            )
        page.update()

    atualizar_clientes_dd()

    produtos_dd = ft.Dropdown(label="Produto", width=300)
    marcas_dd = ft.Dropdown(label="Marca", width=300)
    qtd_ped = ft.TextField(
        label="Quantidade", width=150, keyboard_type="number", value="1"
    )
    obs_ped = ft.TextField(label="Observação", width=300)

    pedido_itens = ft.ListView(spacing=8, expand=True)
    total_texto = ft.Text("Total: R$ 0,00", size=16, weight="bold", color=COR_PRIMARIA)

    total_atual = [0]
    itens_pedido = []

    def atualizar_produtos_dd(e=None):
        produtos_dd.options.clear()
        for prod in listar_produtos():
            produtos_dd.options.append(
                ft.dropdown.Option(str(prod["id"]), prod["nome"])
            )
        page.update()

    def atualizar_marcas_dd(e=None):
        marcas_dd.options.clear()
        if produtos_dd.value:
            for marca in listar_marcas_produto(int(produtos_dd.value)):
                marcas_dd.options.append(
                    ft.dropdown.Option(
                        str(marca["id"]),
                        f"{marca['marca']} (R$ {marca['preco_unitario']:.2f})",
                    )
                )
        page.update()

    produtos_dd.on_change = atualizar_marcas_dd
    atualizar_produtos_dd()

    def adicionar_item(e):
        if not clientes_lista_dd.value or not marcas_dd.value:
            return

        try:
            qtd = int(qtd_ped.value or 1)
            marca_id = int(marcas_dd.value)
            marcas = listar_marcas_produto(int(produtos_dd.value))
            marca_info = [m for m in marcas if m["id"] == marca_id][0]
            subtotal = qtd * marca_info["preco_unitario"]

            item = {
                "marca_id": marca_id,
                "nome": marcas_dd.value,
                "qtd": qtd,
                "preco": marca_info["preco_unitario"],
                "subtotal": subtotal,
            }
            itens_pedido.append(item)

            idx = len(pedido_itens.controls)
            pedido_itens.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(f"{item['nome']} x {qtd}", weight="bold"),
                                    ft.Text(
                                        f"R$ {subtotal:.2f}",
                                        size=12,
                                        color=COR_PRIMARIA,
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.IconButton(
                                ft.icons.DELETE, on_click=lambda: remover_item(idx)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=10,
                    bgcolor=ft.Colors.GREY_100,
                    border_radius=5,
                )
            )

            total_atual[0] += subtotal
            total_texto.value = f"Total: R$ {total_atual[0]:.2f}"

            qtd_ped.value = "1"
            obs_ped.value = ""
            page.update()
        except:
            pass

    def remover_item(idx):
        if 0 <= idx < len(pedido_itens.controls) and 0 <= idx < len(itens_pedido):
            item = itens_pedido.pop(idx)
            total_atual[0] -= item["subtotal"]
            total_texto.value = f"Total: R$ {total_atual[0]:.2f}"
            pedido_itens.controls.pop(idx)
            page.update()

    def salvar_pedido(e):
        if not clientes_lista_dd.value or not itens_pedido:
            return

        sucesso, msg, pedido_id = inserir_pedido(int(clientes_lista_dd.value))
        if sucesso:
            for item in itens_pedido:
                adicionar_item_pedido(
                    pedido_id, item["marca_id"], item["qtd"], item["preco"]
                )

            pedido_itens.controls.clear()
            itens_pedido.clear()
            total_atual[0] = 0
            total_texto.value = "Total: R$ 0,00"
            clientes_lista_dd.value = ""
            atualizar_clientes_dd()
            page.update()

    tela = ft.Column(
        [
            ft.Text("📋 Registrar Pedidos", size=22, weight="bold", color=COR_PRIMARIA),
            ft.Divider(),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            clientes_lista_dd,
                            ft.Row([produtos_dd, marcas_dd], wrap=True),
                            ft.Row([qtd_ped, obs_ped], wrap=True),
                            ft.ElevatedButton(
                                "➕ Adicionar Item",
                                on_click=adicionar_item,
                                color=ft.Colors.WHITE,
                                bgcolor=COR_PRIMARIA,
                                width=300,
                                height=40,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                )
            ),
            ft.Text("Itens do Pedido", size=16, weight="bold", color=COR_PRIMARIA),
            ft.Container(content=pedido_itens, expand=True, height=300),
            total_texto,
            ft.ElevatedButton(
                "💾 Salvar Pedido",
                on_click=salvar_pedido,
                color=ft.Colors.WHITE,
                bgcolor=COR_PRIMARIA,
                width=300,
                height=50,
            ),
        ],
        spacing=15,
        expand=True,
        scroll="auto",
    )

    return tela


# ===== FUNÇÃO PRINCIPAL =====
def main(page: ft.Page):
    page.title = "🌳 Arvoredo - Sistema de Estoque"
    page.window.width = 1400
    page.window.height = 850
    page.theme_mode = "light"
    page.bgcolor = COR_SECUNDARIA

    inicializar_db()

    # Container principal
    conteudo = ft.Column(expand=True, scroll="auto")

    # Dicionário de telas
    telas = {}

    def mudar_tela(tela_nome):
        global tela_atual
        tela_atual = tela_nome
        conteudo.controls.clear()
        conteudo.controls.append(telas[tela_nome])
        page.update()

    # Criar todas as telas
    tela_cadastro = criar_tela_cadastro(
        page,
        lambda: (
            tela_cadastro.atualizar() if hasattr(tela_cadastro, "atualizar") else None
        ),
    )
    telas["cadastro"] = tela_cadastro
    telas["editar"] = criar_tela_editar(page)
    telas["vendas"] = criar_tela_vendas(page)
    telas["clientes"] = criar_tela_clientes(page)
    telas["pedidos"] = criar_tela_pedidos(page)

    # Carregar tela inicial
    conteudo.controls.append(telas["cadastro"])

    # Adicionar ao page
    page.add(
        criar_header(page, mudar_tela),
        ft.Divider(height=5, color=COR_PRIMARIA),
        ft.Container(content=conteudo, expand=True, padding=15),
    )


if __name__ == "__main__":
    ft.run(main)
