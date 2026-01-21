import flet as ft
import sqlite3
from datetime import datetime


# ===== BANCO DE DADOS =====
def inicializar_db():
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo TEXT UNIQUE,
            preco REAL,
            quantidade INTEGER,
            categoria TEXT,
            estoque_minimo INTEGER DEFAULT 5,
            data_cadastro TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def inserir_produto(nome, codigo, preco, qtd, categoria, minimo):
    try:
        conn = sqlite3.connect("estoque.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO produtos (nome, codigo, preco, quantidade, categoria, estoque_minimo, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                nome,
                codigo,
                preco,
                qtd,
                categoria,
                minimo,
                datetime.now().strftime("%Y-%m-%d"),
            ),
        )
        conn.commit()
        conn.close()
        return True, "Produto cadastrado!"
    except sqlite3.IntegrityError:
        return False, "Código já existe!"
    except Exception as e:
        return False, f"Erro: {str(e)}"


def listar_produtos(categoria=None):
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    if categoria:
        cursor.execute("SELECT * FROM produtos WHERE categoria = ?", (categoria,))
    else:
        cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos


def atualizar_estoque(codigo, nova_qtd):
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE produtos SET quantidade = ? WHERE codigo = ?", (nova_qtd, codigo)
    )
    conn.commit()
    conn.close()


# ===== INTERFACE FLET =====
def main(page: ft.Page):
    page.title = "Gestão Estoque - Mercado/Lancheria"
    page.window.width = 1000
    page.window.height = 700
    page.theme_mode = "light"

    inicializar_db()

    # ===== COMPONENTES =====
    nome_field = ft.TextField(label="Nome Produto", width=300)
    codigo_field = ft.TextField(label="Código", width=150)
    preco_field = ft.TextField(label="Preço (R$)", width=120, keyboard_type="number")
    qtd_field = ft.TextField(label="Quantidade", width=120, keyboard_type="number")
    minimo_field = ft.TextField(
        label="Estoque Mínimo", width=120, value="5", keyboard_type="number"
    )

    categoria_dropdown = ft.Dropdown(
        label="Categoria",
        width=200,
        options=[
            ft.dropdown.Option("mercado"),
            ft.dropdown.Option("lancheria"),
        ],
        value="mercado",
    )

    tabela_produtos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código", weight="bold")),
            ft.DataColumn(ft.Text("Nome", weight="bold")),
            ft.DataColumn(ft.Text("Preço", weight="bold")),
            ft.DataColumn(ft.Text("Qtd", weight="bold")),
            ft.DataColumn(ft.Text("Categoria", weight="bold")),
            ft.DataColumn(ft.Text("Status", weight="bold")),
        ],
        rows=[],
    )

    filtro_categoria = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="todos", label="Todos"),
                ft.Radio(value="mercado", label="Mercado"),
                ft.Radio(value="lancheria", label="Lancheria"),
            ]
        ),
        value="todos",
    )

    # ===== FUNÇÕES =====
    def atualizar_tabela(e=None):
        cat = filtro_categoria.value
        produtos = listar_produtos(None if cat == "todos" else cat)

        tabela_produtos.rows.clear()
        for p in produtos:
            # p = (id, nome, codigo, preco, qtd, categoria, estoque_min, data)
            status = "🔴 BAIXO" if p[4] <= p[6] else "🟢 OK"
            cor = ft.Colors.RED_100 if p[4] <= p[6] else None

            tabela_produtos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p[2])),  # codigo
                        ft.DataCell(ft.Text(p[1])),  # nome
                        ft.DataCell(ft.Text(f"R$ {p[3]:.2f}")),
                        ft.DataCell(ft.Text(str(p[4]))),
                        ft.DataCell(ft.Text(p[5])),
                        ft.DataCell(ft.Text(status)),
                    ],
                    color=cor,
                )
            )
        page.update()

    def cadastrar_produto(e):
        # Validações simples
        if not nome_field.value or not codigo_field.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Preencha nome e código!"), bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            preco = float(preco_field.value or 0)
            qtd = int(qtd_field.value or 0)
            minimo = int(minimo_field.value or 5)
        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Preço/quantidade inválidos!"), bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        sucesso, msg = inserir_produto(
            nome_field.value,
            codigo_field.value,
            preco,
            qtd,
            categoria_dropdown.value,
            minimo,
        )

        # Feedback visual
        page.snack_bar = ft.SnackBar(
            ft.Text(msg), bgcolor=ft.Colors.GREEN if sucesso else ft.Colors.RED
        )
        page.snack_bar.open = True

        if sucesso:
            # Limpar campos
            nome_field.value = ""
            codigo_field.value = ""
            preco_field.value = ""
            qtd_field.value = ""
            minimo_field.value = "5"
            atualizar_tabela()

        page.update()

    # ===== LAYOUT =====
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    # HEADER
                    ft.Container(
                        content=ft.Text(
                            "📦 Sistema de Estoque - Arvoredo",
                            size=28,
                            weight="bold",
                            color=ft.Colors.WHITE,
                        ),
                        bgcolor="#2d8f4c",
                        padding=20,
                        border_radius=10,
                    ),
                    ft.Divider(height=20, color="transparent"),
                    # CADASTRO
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Cadastrar Produto", size=20, weight="bold"
                                    ),
                                    ft.Row(
                                        [
                                            nome_field,
                                            codigo_field,
                                            preco_field,
                                            qtd_field,
                                            minimo_field,
                                            categoria_dropdown,
                                        ],
                                        wrap=True,
                                    ),
                                    ft.ElevatedButton(
                                        "➕ Cadastrar",
                                        on_click=cadastrar_produto,
                                        color=ft.Colors.WHITE,
                                        bgcolor="#2d8f4c",
                                    ),
                                ]
                            ),
                            padding=20,
                        )
                    ),
                    ft.Divider(height=20, color="transparent"),
                    # LISTAGEM
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                "Produtos Cadastrados",
                                                size=20,
                                                weight="bold",
                                            ),
                                            filtro_categoria,
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                tabela_produtos,
                                            ],
                                            scroll="auto",
                                        ),
                                        height=300,
                                    ),
                                    ft.ElevatedButton(
                                        "🔄 Atualizar Lista",
                                        on_click=atualizar_tabela,
                                    ),
                                ]
                            ),
                            padding=20,
                        )
                    ),
                ],
                spacing=10,
            ),
            padding=20,
        )
    )

    # Carregar produtos iniciais
    atualizar_tabela()


# Rodar app
ft.run(main)
