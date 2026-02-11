"""
Tela de Edição de Produtos com Tabela tipo Explorer
"""

import flet as ft
from database import (
    get_connection,
    listar_produtos,
    listar_marcas_produto,
    atualizar_quantidade_marca,
)
from ui.componentes import COR_PRIMARIA


def criar_tela_editar(page):
    """Tela para editar produtos com tabela tipo explorer"""

    # Estado da tabela
    estado_tabela = {
        "ordem_coluna": None,
        "crescente": True,
        "linhas_selecionadas": set(),
        "ultima_clicada": None,
        "todos_dados": [],
    }

    def get_dados_tabela():
        """Retorna lista de dados para a tabela"""
        dados = []
        produtos = listar_produtos()

        for prod in produtos:
            marcas = listar_marcas_produto(prod["id"])
            for marca in marcas:
                dados.append(
                    {
                        "produto_id": prod["id"],
                        "marca_id": marca["id"],
                        "nome": prod["nome"],
                        "marca": marca["marca"],
                        "valor": marca["preco_unitario"],
                        "categoria": prod["categoria"],
                        "estoque": marca["quantidade"],
                        "validade": marca["data_validade"] or "N/A",
                        "data_registro": marca["data_cadastro"] or "N/A",
                    }
                )

        return dados

    def ordenar_dados(dados, coluna, crescente=True):
        """Ordena dados pela coluna especificada"""
        map_colunas = {
            "Nome": "nome",
            "Marca": "marca",
            "Valor": "valor",
            "Categoria": "categoria",
            "Estoque": "estoque",
            "Validade": "validade",
            "Data Registro": "data_registro",
        }

        chave = map_colunas.get(coluna, "nome")

        if chave == "valor":
            return sorted(
                dados,
                key=lambda x: float(x[chave]),
                reverse=not crescente,
            )
        elif chave == "estoque":
            return sorted(
                dados,
                key=lambda x: int(x[chave]),
                reverse=not crescente,
            )
        else:
            return sorted(
                dados,
                key=lambda x: str(x[chave]).lower(),
                reverse=not crescente,
            )

    def abrir_editor(indice):
        """Abre modal para editar o produto"""
        if indice >= len(estado_tabela["todos_dados"]):
            return

        item = estado_tabela["todos_dados"][indice]
        marca_id = item["marca_id"]
        marca_nome = item["marca"]
        preco = item["valor"]
        estoque = item["estoque"]
        validade = item["validade"]

        novo_preco = ft.TextField(
            label="Preço Unitário", value=str(preco), keyboard_type="number"
        )
        novo_estoque = ft.TextField(
            label="Quantidade", value=str(estoque), keyboard_type="number"
        )
        nova_validade = ft.TextField(label="Validade (DD/MM/YYYY)", value=validade)

        def salvar_edicao(e):
            try:
                novo_preco_val = float(novo_preco.value or preco)
                novo_estoque_val = int(novo_estoque.value or estoque)
                nova_validade_val = nova_validade.value or validade

                atualizar_quantidade_marca(marca_id, novo_estoque_val)

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE produto_marcas SET preco_unitario = ?, data_validade = ? WHERE id = ?",
                    (novo_preco_val, nova_validade_val, marca_id),
                )
                conn.commit()
                conn.close()

                page.snack_bar = ft.SnackBar(
                    ft.Text(f"✅ {marca_nome} atualizado com sucesso!")
                )
                page.snack_bar.open = True

                dlg.open = False
                atualizar_tabela()
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
                atualizar_tabela()
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
                    nova_validade,
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

    def criar_tabela():
        """Cria a tabela com as linhas de dados"""
        dados = get_dados_tabela()
        estado_tabela["todos_dados"] = dados

        if estado_tabela["ordem_coluna"]:
            dados = ordenar_dados(
                dados, estado_tabela["ordem_coluna"], estado_tabela["crescente"]
            )
            estado_tabela["todos_dados"] = dados

        def ordenar_coluna(nome_coluna):
            """Alterna ordenação da coluna"""
            if estado_tabela["ordem_coluna"] == nome_coluna:
                estado_tabela["crescente"] = not estado_tabela["crescente"]
            else:
                estado_tabela["ordem_coluna"] = nome_coluna
                estado_tabela["crescente"] = True
            atualizar_tabela()

        colunas = [
            ft.DataColumn(
                ft.Text("Nome", weight="bold", size=11),
                on_sort=lambda e: ordenar_coluna("Nome"),
            ),
            ft.DataColumn(
                ft.Text("Marca", weight="bold", size=11),
                on_sort=lambda e: ordenar_coluna("Marca"),
            ),
            ft.DataColumn(
                ft.Text("Valor", weight="bold", size=11),
                numeric=True,
                on_sort=lambda e: ordenar_coluna("Valor"),
            ),
            ft.DataColumn(
                ft.Text("Categoria", weight="bold", size=11),
                on_sort=lambda e: ordenar_coluna("Categoria"),
            ),
            ft.DataColumn(
                ft.Text("Estoque", weight="bold", size=11),
                numeric=True,
                on_sort=lambda e: ordenar_coluna("Estoque"),
            ),
            ft.DataColumn(
                ft.Text("Validade", weight="bold", size=11),
                on_sort=lambda e: ordenar_coluna("Validade"),
            ),
            ft.DataColumn(
                ft.Text("Data Registro", weight="bold", size=11),
                on_sort=lambda e: ordenar_coluna("Data Registro"),
            ),
        ]

        linhas = []
        for idx, item in enumerate(dados):

            def handle_selection(e, indice=idx):
                """Handler para seleção de linhas"""
                if indice in estado_tabela["linhas_selecionadas"]:
                    # Se já está selecionada, abre editor
                    abrir_editor(indice)
                else:
                    # Senão, seleciona
                    estado_tabela["linhas_selecionadas"].clear()
                    estado_tabela["linhas_selecionadas"].add(indice)
                    estado_tabela["ultima_clicada"] = indice
                    atualizar_tabela()

            linhas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["nome"], size=11)),
                        ft.DataCell(ft.Text(item["marca"], size=11)),
                        ft.DataCell(ft.Text(f"R$ {item['valor']:.2f}", size=11)),
                        ft.DataCell(ft.Text(item["categoria"], size=11)),
                        ft.DataCell(ft.Text(str(item["estoque"]), size=11)),
                        ft.DataCell(ft.Text(item["validade"], size=11)),
                        ft.DataCell(ft.Text(item["data_registro"], size=11)),
                    ],
                    selected=idx in estado_tabela["linhas_selecionadas"],
                    on_select_change=lambda e, indice=idx: handle_selection(e, indice),
                )
            )

        tabela = ft.DataTable(
            columns=colunas,
            rows=linhas,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            show_checkbox_column=True,
            heading_row_color=COR_PRIMARIA,
            heading_row_height=50,
            data_row_max_height=40,
            width=1200,
            horizontal_lines=ft.CrossAxisAlignment.START,
        )

        return tabela

    def atualizar_tabela():
        """Atualiza a tabela na tela"""
        tabela_container.content = criar_tabela()
        page.update()

    tabela_container = ft.Column(
        [criar_tabela()],
        scroll="auto",
        expand=True,
    )

    def editar_selecionadas(e):
        """Edita as linhas selecionadas"""
        if not estado_tabela["linhas_selecionadas"]:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Selecione pelo menos uma linha"))
            page.snack_bar.open = True
            page.update()
            return

        indice = min(estado_tabela["linhas_selecionadas"])
        abrir_editor(indice)

    def deletar_selecionadas(e):
        """Deleta as linhas selecionadas"""
        if not estado_tabela["linhas_selecionadas"]:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Selecione pelo menos uma linha"))
            page.snack_bar.open = True
            page.update()
            return

        indices = sorted(estado_tabela["linhas_selecionadas"], reverse=True)
        for indice in indices:
            if indice < len(estado_tabela["todos_dados"]):
                item = estado_tabela["todos_dados"][indice]
                marca_id = item["marca_id"]
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM produto_marcas WHERE id = ?", (marca_id,)
                    )
                    conn.commit()
                    conn.close()
                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {str(ex)}"))
                    page.snack_bar.open = True
                    page.update()
                    return

        page.snack_bar = ft.SnackBar(
            ft.Text(f"✅ {len(indices)} item(ns) deletado(s) com sucesso!")
        )
        page.snack_bar.open = True

        estado_tabela["linhas_selecionadas"].clear()
        atualizar_tabela()

    info_texto = ft.Text(
        "💡 Clique nas colunas para ordenar | Clique sobre uma linha para selecioná-la | Clique novamente na linha selecionada para editar",
        size=10,
        color=ft.Colors.GREY_700,
    )

    tela = ft.Column(
        [
            ft.Text("✏️ Editar Produtos", size=22, weight="bold", color=COR_PRIMARIA),
            ft.Divider(),
            info_texto,
            ft.Row(
                [
                    ft.ElevatedButton(
                        "✏️ Editar Selecionada",
                        on_click=editar_selecionadas,
                        color=ft.Colors.WHITE,
                        bgcolor=COR_PRIMARIA,
                    ),
                    ft.ElevatedButton(
                        "🗑️ Deletar Selecionadas",
                        on_click=deletar_selecionadas,
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED,
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(),
            ft.Container(content=tabela_container, expand=True),
        ],
        spacing=15,
        expand=True,
    )

    return tela
