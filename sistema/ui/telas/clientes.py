"""
Tela de Clientes/Fiados
"""
import flet as ft
from database import (
    inserir_cliente,
    listar_clientes,
    listar_pedidos_cliente,
)
from ui.componentes import COR_PRIMARIA

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
