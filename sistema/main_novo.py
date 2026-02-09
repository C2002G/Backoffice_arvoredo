"""
Main - Sistema Arvoredo
Arquivo principal - orquestra as telas
"""
import flet as ft
from database import inicializar_db
from ui.componentes import criar_header, COR_PRIMARIA, COR_SECUNDARIA
from ui.telas.cadastro import criar_tela_cadastro
from ui.telas.editar import criar_tela_editar
from ui.telas.vendas import criar_tela_vendas
from ui.telas.clientes import criar_tela_clientes
from ui.telas.pedidos import criar_tela_pedidos

# ===== VARIÁVEIS GLOBAIS =====
tela_atual = "cadastro"


def main(page: ft.Page):
    """Função principal da aplicação"""
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
        """Muda entre as telas"""
        global tela_atual
        tela_atual = tela_nome
        conteudo.controls.clear()
        conteudo.controls.append(telas[tela_nome])
        page.update()

    # Criar todas as telas com os callbacks necessários
    tela_cadastro = criar_tela_cadastro(
        page,
        lambda: (
            tela_cadastro.atualizar() if hasattr(tela_cadastro, "atualizar") else None
        ),
        mudar_tela,
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
