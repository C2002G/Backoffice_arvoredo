import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

DB_NAME = "arvoredo.db"


def get_connection():
    """Retorna conexão com banco de dados"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_db():
    """Inicializa o banco de dados com todas as tabelas"""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de produtos (agrupados por nome)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade_total INTEGER DEFAULT 0,
            valor_total REAL DEFAULT 0,
            data_criacao TEXT
        )
    """
    )

    # Tabela de variações de produtos por marca
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS produto_marcas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            codigo TEXT UNIQUE,
            marca TEXT NOT NULL,
            preco_unitario REAL NOT NULL,
            quantidade INTEGER DEFAULT 0,
            data_cadastro TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """
    )

    # Tabela de histórico de entrada/saída
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS historico_movimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_marca_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_hora TEXT,
            motivo TEXT,
            FOREIGN KEY (produto_marca_id) REFERENCES produto_marcas(id)
        )
    """
    )

    # Tabela de clientes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            apelido TEXT,
            cpf TEXT,
            fiando INTEGER DEFAULT 0,
            data_criacao TEXT
        )
    """
    )

    # Tabela de pedidos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data_hora TEXT,
            status TEXT DEFAULT 'pendente',
            total REAL DEFAULT 0,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """
    )

    # Tabela de itens do pedido
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pedido_itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_marca_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            observacao TEXT,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (produto_marca_id) REFERENCES produto_marcas(id)
        )
    """
    )

    conn.commit()
    conn.close()


# ===== FUNÇÕES DE PRODUTOS =====


def inserir_produto(nome: str, categoria: str) -> Tuple[bool, str, int]:
    """Insere um novo produto (agrupado por nome)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, categoria, data_criacao) VALUES (?, ?, ?)",
            (nome, categoria, datetime.now().strftime("%d/%m/%Y %H:%M")),
        )
        conn.commit()
        produto_id = cursor.lastrowid
        conn.close()
        return True, "Produto cadastrado!", produto_id
    except Exception as e:
        return False, f"Erro: {str(e)}", -1


def inserir_marca_produto(
    produto_id: int, codigo: str, marca: str, preco: float
) -> Tuple[bool, str]:
    """Insere uma marca específica de um produto"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO produto_marcas (produto_id, codigo, marca, preco_unitario, data_cadastro)
               VALUES (?, ?, ?, ?, ?)""",
            (
                produto_id,
                codigo,
                marca,
                preco,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
            ),
        )
        conn.commit()
        marca_id = cursor.lastrowid
        conn.close()
        return True, "Marca adicionada!", marca_id
    except sqlite3.IntegrityError:
        return False, "Código já existe!"
    except Exception as e:
        return False, f"Erro: {str(e)}", -1


def listar_produtos() -> List:
    """Lista todos os produtos com quantidade e valor total"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.nome, p.categoria, 
               COUNT(pm.id) as total_marcas,
               SUM(pm.quantidade) as quantidade_total,
               SUM(pm.quantidade * pm.preco_unitario) as valor_total
        FROM produtos p
        LEFT JOIN produto_marcas pm ON p.id = pm.produto_id
        GROUP BY p.id
        ORDER BY p.nome
    """
    )
    produtos = cursor.fetchall()
    conn.close()
    return produtos


def listar_marcas_produto(produto_id: int) -> List:
    """Lista todas as marcas de um produto com seu histórico"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT pm.id, pm.codigo, pm.marca, pm.preco_unitario, pm.quantidade, pm.data_cadastro
        FROM produto_marcas pm
        WHERE pm.produto_id = ?
        ORDER BY pm.marca
    """,
        (produto_id,),
    )
    marcas = cursor.fetchall()
    conn.close()
    return marcas


def atualizar_quantidade_marca(marca_id: int, nova_quantidade: int) -> Tuple[bool, str]:
    """Atualiza quantidade de uma marca específica"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produto_marcas SET quantidade = ? WHERE id = ?",
            (nova_quantidade, marca_id),
        )
        conn.commit()
        conn.close()
        return True, "Quantidade atualizada!"
    except Exception as e:
        return False, f"Erro: {str(e)}"


def adicionar_historico(
    marca_id: int, tipo: str, quantidade: int, motivo: str = ""
) -> Tuple[bool, str]:
    """Registra entrada/saída no histórico"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO historico_movimentacao (produto_marca_id, tipo, quantidade, data_hora, motivo)
               VALUES (?, ?, ?, ?, ?)""",
            (
                marca_id,
                tipo,
                quantidade,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                motivo,
            ),
        )
        conn.commit()
        conn.close()
        return True, "Histórico registrado!"
    except Exception as e:
        return False, f"Erro: {str(e)}"


def listar_historico_marca(marca_id: int) -> List:
    """Lista histórico de movimentação de uma marca"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM historico_movimentacao WHERE produto_marca_id = ? ORDER BY data_hora DESC""",
        (marca_id,),
    )
    historico = cursor.fetchall()
    conn.close()
    return historico


# ===== FUNÇÕES DE CLIENTES =====


def inserir_cliente(
    nome: str, apelido: str = "", cpf: str = "", fiando: bool = False
) -> Tuple[bool, str, int]:
    """Insere um novo cliente"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO clientes (nome, apelido, cpf, fiando, data_criacao)
               VALUES (?, ?, ?, ?, ?)""",
            (
                nome,
                apelido,
                cpf,
                1 if fiando else 0,
                datetime.now().strftime("%d/%m/%Y"),
            ),
        )
        conn.commit()
        cliente_id = cursor.lastrowid
        conn.close()
        return True, "Cliente cadastrado!", cliente_id
    except Exception as e:
        return False, f"Erro: {str(e)}", -1


def listar_clientes() -> List:
    """Lista todos os clientes"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY nome")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


def obter_cliente(cliente_id: int) -> Optional[dict]:
    """Obtém dados de um cliente específico"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return dict(cliente) if cliente else None


# ===== FUNÇÕES DE PEDIDOS =====


def inserir_pedido(cliente_id: int) -> Tuple[bool, str, int]:
    """Cria um novo pedido"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, data_hora) VALUES (?, ?)",
            (cliente_id, datetime.now().strftime("%d/%m/%Y %H:%M")),
        )
        conn.commit()
        pedido_id = cursor.lastrowid
        conn.close()
        return True, "Pedido criado!", pedido_id
    except Exception as e:
        return False, f"Erro: {str(e)}", -1


def adicionar_item_pedido(
    pedido_id: int,
    marca_id: int,
    quantidade: int,
    preco_unitario: float,
    observacao: str = "",
) -> Tuple[bool, str]:
    """Adiciona um item ao pedido"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        subtotal = quantidade * preco_unitario
        cursor.execute(
            """INSERT INTO pedido_itens (pedido_id, produto_marca_id, quantidade, preco_unitario, subtotal, observacao)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (pedido_id, marca_id, quantidade, preco_unitario, subtotal, observacao),
        )
        # Atualizar total do pedido
        cursor.execute(
            "SELECT SUM(subtotal) FROM pedido_itens WHERE pedido_id = ?", (pedido_id,)
        )
        total = cursor.fetchone()[0] or 0
        cursor.execute("UPDATE pedidos SET total = ? WHERE id = ?", (total, pedido_id))
        conn.commit()
        conn.close()
        return True, "Item adicionado!"
    except Exception as e:
        return False, f"Erro: {str(e)}"


def listar_pedidos_cliente(cliente_id: int) -> List:
    """Lista pedidos de um cliente"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM pedidos WHERE cliente_id = ? ORDER BY data_hora DESC",
        (cliente_id,),
    )
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos


def listar_itens_pedido(pedido_id: int) -> List:
    """Lista itens de um pedido específico"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT pi.*, pm.marca, p.nome 
           FROM pedido_itens pi
           JOIN produto_marcas pm ON pi.produto_marca_id = pm.id
           JOIN produtos p ON pm.produto_id = p.id
           WHERE pi.pedido_id = ?""",
        (pedido_id,),
    )
    itens = cursor.fetchall()
    conn.close()
    return itens


def listar_vendas() -> List:
    """Lista histórico de vendas com informações do cliente"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT pi.*, p.nome, pm.marca, pm.data_cadastro, c.nome as cliente
        FROM pedido_itens pi
        JOIN produto_marcas pm ON pi.produto_marca_id = pm.id
        JOIN produtos p ON pm.produto_id = p.id
        JOIN pedidos pe ON pi.pedido_id = pe.id
        JOIN clientes c ON pe.cliente_id = c.id
        ORDER BY pe.data_hora DESC
    """
    )
    vendas = cursor.fetchall()
    conn.close()
    return vendas
