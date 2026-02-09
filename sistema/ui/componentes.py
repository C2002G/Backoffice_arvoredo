"""
Componentes compartilhados e estilos globais
"""

import flet as ft

# ===== CORES GLOBAIS =====
COR_PRIMARIA = "#2d8f4c"  # Verde Arvoredo
COR_PRIMARIA_ESCURA = "#1f6336"
COR_SECUNDARIA = "#f5f5f5"


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
