from __future__ import annotations

from functools import wraps
from datetime import datetime
from typing import Callable, Any


# TUPLE + SET (categorias)
CATEGORIAS_PADRAO: tuple[str, ...] = (
    "Alimentação", "Transporte", "Casa", "Saúde", "Educação", "Lazer", "Outros"
)
CATEGORIAS_VALIDAS: set[str] = set(CATEGORIAS_PADRAO)


def log_acao(acao: str) -> Callable:
    """Decorador simples para registar ações no terminal."""
    def deco(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[LOG] {acao} -> {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return deco


def _parse_data_flexivel(data_str: str):
    """
    Aceita:
    - 'AAAA-MM-DD' (input type=date do HTML)
    - 'DD/MM/AAAA'
    - 'DD-MM-AAAA'
    - 'AAAA/MM/DD'
    """
    if data_str is None:
        data_str = ""

    s = data_str.strip()
    if not s:
        raise ValueError("Data não foi enviada. Escolhe uma data no calendário.")

    formatos = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d")
    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass

    raise ValueError("Data inválida. Use AAAA-MM-DD (ex.: 2026-02-03) ou DD/MM/AAAA.")


def validar_despesa(func: Callable) -> Callable:
    """
    Decorador para validar os campos da despesa.
    Este decorador espera receber data_str, descricao, categoria, valor_str em kwargs.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        data_str = kwargs.get("data_str", "")
        descricao = (kwargs.get("descricao") or "").strip()
        categoria = (kwargs.get("categoria") or "").strip()
        valor_str = (kwargs.get("valor_str") or "").strip()

        # DATA
        data_obj = _parse_data_flexivel(data_str)

        # DESCRIÇÃO
        if len(descricao) < 2:
            raise ValueError("Descrição muito curta. Escreve pelo menos 2 caracteres.")

        # CATEGORIA
        if categoria not in CATEGORIAS_VALIDAS:
            raise ValueError("Categoria inválida. Escolhe uma das opções do menu.")

        # VALOR (aceita vírgula)
        valor_str = valor_str.replace(",", ".")
        try:
            valor = float(valor_str)
        except ValueError:
            raise ValueError("Valor inválido. Ex.: 12,50 ou 12.50")

        if valor <= 0:
            raise ValueError("O valor deve ser maior que 0.")

        # Injecta valores já validados
        kwargs["data_obj"] = data_obj
        kwargs["descricao"] = descricao
        kwargs["categoria"] = categoria
        kwargs["valor"] = valor

        return func(*args, **kwargs)

    return wrapper
