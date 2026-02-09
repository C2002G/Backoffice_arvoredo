"""
Tela de Registro de Pedidos
"""

import flet as ft
from database import (
    listar_clientes,
    listar_produtos,
    listar_marcas_produto,
    inserir_pedido,
    adicionar_item_pedido,
)
from ui.componentes import COR_PRIMARIA


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
