"""
Tela de Registro de Vendas
"""
import flet as ft
from database import listar_vendas
from ui.componentes import COR_PRIMARIA

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
