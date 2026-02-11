"""
Tela de Cadastro de Produtos
"""

import flet as ft
from database import (
    listar_produtos,
    inserir_produto,
    listar_marcas_produto,
    inserir_marca_produto,
    atualizar_quantidade_marca,
)
from ui.componentes import COR_PRIMARIA


def criar_tela_cadastro(page, atualizar_fn, mudar_tela_fn):
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
    validade = ft.TextField(
        label="Validade (DD/MM/YYYY)", width=150, hint_text="Ex: 31/12/2025"
    )

    msg_status = ft.Text("", color=ft.Colors.RED)

    def cadastrar(e):
        if (
            not nome_prod.value
            or not categoria_dd.value
            or not marca_nome.value
            or not validade.value
        ):
            msg_status.value = "❌ Preencha todos os campos!"
            msg_status.color = ft.Colors.RED
            page.update()
            return

        # Verificar se produto já existe
        produtos = listar_produtos()
        produto_existente = None
        for prod in produtos:
            if prod["nome"].lower() == nome_prod.value.lower():
                produto_existente = prod
                break

        # Se existe, usa o ID dele; senão, cria novo
        if produto_existente:
            prod_id = produto_existente["id"]
            msg_status.value = (
                f"✅ Adicionando marca ao produto existente: {nome_prod.value}"
            )
            msg_status.color = ft.Colors.GREEN
        else:
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
            validade.value,
        )

        if sucesso2 and marca_id != -1:
            # Atualizar quantidade
            atualizar_quantidade_marca(marca_id, int(qtd_marca.value or 0))
            msg_status.value = (
                f"✅ Marca adicionada: {nome_prod.value} - {marca_nome.value}"
            )
            msg_status.color = ft.Colors.GREEN

            # Limpar campos
            nome_prod.value = ""
            categoria_dd.value = ""
            marca_nome.value = ""
            preco_un.value = ""
            qtd_marca.value = "0"
            codigo_marca.value = ""
            validade.value = ""

            atualizar_fn()
        else:
            msg_status.value = f"❌ {msg2}"
            msg_status.color = ft.Colors.RED

        page.update()

    # Listar produtos
    produtos_list = ft.ListView(spacing=10, expand=True)

    def editar_produto(produto_id):
        """Navega para tela de editar com produto selecionado"""
        mudar_tela_fn("editar")

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
                                        f"Marca: {marcas_texto}",
                                        size=11,
                                        color=ft.Colors.GREY_700,
                                    ),
                                    ft.Text(
                                        f"Total: {prod['quantidade_total'] or 0} un | Valor: R$ {prod['valor_total'] or 0:.2f}",
                                        weight="bold",
                                        color=COR_PRIMARIA,
                                    ),
                                    ft.Text(
                                        f"Data Registro: {prod['data_criacao'] or 'N/A'} | Validade: {', '.join([m['data_validade'] or 'N/A' for m in marcas]) if marcas else 'N/A'}",
                                        size=10,
                                        color=ft.Colors.GREY_700,
                                    ),
                                ],
                                spacing=5,
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                "✏️ Editar",
                                width=80,
                                height=40,
                                on_click=lambda e, pid=prod["id"]: editar_produto(pid),
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
                            ft.Row([validade], wrap=True),
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
