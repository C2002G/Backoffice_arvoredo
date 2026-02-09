"""
Tela de Edição de Produtos
"""
import flet as ft
from database import (
    get_connection,
    listar_produtos,
    listar_marcas_produto,
    listar_historico_marca,
    atualizar_quantidade_marca,
)
from ui.componentes import COR_PRIMARIA

def criar_tela_editar(page):
    """Tela para editar produtos e ver histórico"""

    busca = ft.TextField(label="🔍 Buscar produto...", width=400)
    resultado_lista = ft.ListView(spacing=10, expand=True)

    def abrir_modal_edicao(marca_id, marca_nome, preco, estoque, produto_id):
        """Abre modal para editar marca do produto"""
        novo_preco = ft.TextField(
            label="Preço Unitário", value=str(preco), keyboard_type="number"
        )
        novo_estoque = ft.TextField(
            label="Quantidade", value=str(estoque), keyboard_type="number"
        )

        def salvar_edicao(e):
            try:
                novo_preco_val = float(novo_preco.value or preco)
                novo_estoque_val = int(novo_estoque.value or estoque)

                # Atualizar quantidade
                atualizar_quantidade_marca(marca_id, novo_estoque_val)

                # Atualizar preço
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE produto_marcas SET preco_unitario = ? WHERE id = ?",
                    (novo_preco_val, marca_id),
                )
                conn.commit()
                conn.close()

                page.snack_bar = ft.SnackBar(
                    ft.Text(f"✅ {marca_nome} atualizado com sucesso!")
                )
                page.snack_bar.open = True

                dlg.open = False
                buscar_produtos(None)
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

        def deletar_marca(e):
            """Deleta uma marca do produto"""
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM produto_marcas WHERE id = ?", (marca_id,))
                conn.commit()
                conn.close()

                page.snack_bar = ft.SnackBar(
                    ft.Text(f"✅ {marca_nome} deletado com sucesso!")
                )
                page.snack_bar.open = True

                dlg.open = False
                buscar_produtos(None)
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

        dlg = ft.AlertDialog(
            title=ft.Text(f"Editar: {marca_nome}"),
            content=ft.Column(
                [
                    novo_preco,
                    novo_estoque,
                    ft.Divider(),
                    ft.Text("Ações:", weight="bold"),
                ],
                spacing=10,
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    "Deletar",
                    on_click=deletar_marca,
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                ),
                ft.TextButton("Cancelar", on_click=lambda e: close_dlg()),
                ft.TextButton(
                    "Salvar",
                    on_click=salvar_edicao,
                    style=ft.ButtonStyle(color=ft.Colors.GREEN),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        def close_dlg(e=None):
            dlg.open = False
            page.update()

        page.dialog = dlg
        dlg.open = True
        page.update()

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
                                                    "✏️ Editar",
                                                    width=100,
                                                    height=40,
                                                    on_click=lambda e, mid=marca[
                                                        "id"
                                                    ], mn=marca["marca"], p=marca[
                                                        "preco_unitario"
                                                    ], q=marca[
                                                        "quantidade"
                                                    ]: abrir_modal_edicao(
                                                        mid, mn, p, q, prod_id
                                                    ),
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
