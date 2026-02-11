"""
Tela de Edição Completa do Produto
"""

import flet as ft
from database import get_connection, listar_marcas_produto
from ui.componentes import COR_PRIMARIA


def criar_tela_editar_produto(page, produto_id=None, mudar_tela_fn=None):
    """Tela para editar um produto completo"""

    def voltar_a_editar(e):
        """Volta para a tela de editar"""
        if mudar_tela_fn:
            mudar_tela_fn("editar")
        else:
            # Fallback caso mudar_tela_fn não esteja disponível
            conteudo = page.data.get("conteudo")
            if conteudo:
                from ui.telas.editar import criar_tela_editar

                conteudo.controls.clear()
                conteudo.controls.append(criar_tela_editar(page, mudar_tela_fn))
                page.update()

    if not produto_id:
        return ft.Column(
            [
                ft.Text("Erro: Produto não selecionado", color=ft.Colors.RED),
                ft.ElevatedButton(
                    "✅ Voltar",
                    on_click=voltar_a_editar,
                    color=ft.Colors.WHITE,
                    bgcolor=COR_PRIMARIA,
                ),
            ]
        )

    # Obter informações do produto
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()
    conn.close()

    if not produto:
        return ft.Column(
            [
                ft.Text("Produto não encontrado", color=ft.Colors.RED),
                ft.ElevatedButton(
                    "✅ Voltar",
                    on_click=voltar_a_editar,
                    color=ft.Colors.WHITE,
                    bgcolor=COR_PRIMARIA,
                ),
            ]
        )

    # Campos editáveis
    campo_nome = ft.TextField(
        label="Nome do Produto",
        value=produto["nome"],
        width=400,
    )

    campo_categoria = ft.TextField(
        label="Categoria",
        value=produto["categoria"],
        width=400,
    )

    def salvar_produto(e):
        """Salva as alterações do produto"""
        try:
            if not campo_nome.value.strip():
                page.snack_bar = ft.SnackBar(
                    ft.Text("❌ Nome do produto é obrigatório")
                )
                page.snack_bar.open = True
                page.update()
                return

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE produtos SET nome = ?, categoria = ? WHERE id = ?",
                (campo_nome.value, campo_categoria.value, produto_id),
            )
            conn.commit()
            conn.close()

            page.snack_bar = ft.SnackBar(
                ft.Text(f"✅ {campo_nome.value} atualizado com sucesso!")
            )
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    def deletar_produto(e):
        """Abre diálogo de confirmação para deletar o produto"""

        def confirmar_delecao(e):
            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Deletar todas as marcas do produto
                cursor.execute(
                    "DELETE FROM produto_marcas WHERE produto_id = ?", (produto_id,)
                )

                # Deletar o produto
                cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))

                conn.commit()
                conn.close()

                page.snack_bar = ft.SnackBar(
                    ft.Text(f"✅ {campo_nome.value} deletado com sucesso!")
                )
                page.snack_bar.open = True
                page.update()

                # Voltar para editar após deletar
                voltar_a_editar(None)
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(f"Deletar '{campo_nome.value}'?"),
            content=ft.Column(
                [
                    ft.Text(
                        "Essa ação vai deletar o produto e todas as suas marcas associadas.",
                        color=ft.Colors.RED,
                    ),
                    ft.Text("Tem certeza que deseja continuar?", weight="bold"),
                ],
                spacing=10,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: (setattr(dlg, "open", False), page.update()),
                ),
                ft.TextButton(
                    "Deletar",
                    on_click=confirmar_delecao,
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                ),
            ],
        )

        page.dialog = dlg
        dlg.open = True
        page.update()

    # Obter marcas do produto
    marcas = listar_marcas_produto(produto_id)

    marcas_list = ft.Column(
        [
            ft.Text("Marcas Associadas:", size=14, weight="bold", color=COR_PRIMARIA),
        ]
        + [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(marca["marca"], weight="bold", size=12),
                                ft.Text(
                                    f"Preço: R$ {marca['preco_unitario']:.2f}",
                                    size=11,
                                ),
                                ft.Text(f"Qtd: {marca['quantidade']}", size=11),
                                ft.Text(
                                    f"Validade: {marca['data_validade'] or 'N/A'}",
                                    size=11,
                                ),
                            ],
                            tight=True,
                        ),
                    ],
                    expand=True,
                ),
                padding=10,
                bgcolor=ft.Colors.GREY_100,
                border_radius=5,
            )
            for marca in marcas
        ],
        spacing=10,
        expand=True,
    )

    tela = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "📝 Editar Produto Completo",
                            size=22,
                            weight="bold",
                            color=COR_PRIMARIA,
                        ),
                        ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            icon_size=30,
                            on_click=voltar_a_editar,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(),
                ft.Text("Informações do Produto", size=14, weight="bold"),
                ft.Column(
                    [
                        campo_nome,
                        campo_categoria,
                    ],
                    spacing=15,
                ),
                ft.Divider(),
                ft.Container(
                    content=marcas_list,
                    expand=True,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    padding=15,
                ),
                ft.Divider(),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "✅ Salvar",
                            on_click=salvar_produto,
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREEN,
                        ),
                        ft.ElevatedButton(
                            "🗑️ Deletar Produto",
                            on_click=deletar_produto,
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.RED,
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=15,
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    return tela
