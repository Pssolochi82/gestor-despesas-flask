from __future__ import annotations

import os
from datetime import date

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash

from models import Despesa
from utils import CATEGORIAS_PADRAO, log_acao, validar_despesa

app = Flask(__name__)
app.secret_key = "iefp-segredo-simples"  # para flash messages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "despesas.csv")


def garantir_csv():
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

    # Se não existir, cria com cabeçalho
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=["data", "descricao", "categoria", "valor"])
        df.to_csv(CSV_PATH, index=False)
        return

    # Se existir mas estiver vazio (0 bytes), recria cabeçalho
    if os.path.getsize(CSV_PATH) == 0:
        df = pd.DataFrame(columns=["data", "descricao", "categoria", "valor"])
        df.to_csv(CSV_PATH, index=False)


def ler_df() -> pd.DataFrame:
    garantir_csv()
    df = pd.read_csv(CSV_PATH)

    # Garantir colunas mesmo se algo correr mal no ficheiro
    colunas = ["data", "descricao", "categoria", "valor"]
    for c in colunas:
        if c not in df.columns:
            df[c] = "" if c != "valor" else 0.0
    df = df[colunas]

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0.0)

    return df


def guardar_df(df: pd.DataFrame) -> None:
    df.to_csv(CSV_PATH, index=False)


@app.get("/")
def index():
    df = ler_df()

    categoria_filtro = request.args.get("categoria", "").strip()
    if categoria_filtro:
        df = df[df["categoria"] == categoria_filtro]

    if not df.empty:
        df = df.sort_values(by="data", ascending=False)

    despesas = df.to_dict(orient="records")

    return render_template(
        "index.html",
        despesas=despesas,
        categorias=CATEGORIAS_PADRAO,
        categoria_filtro=categoria_filtro,
        hoje=date.today().isoformat(),
    )


# ✅ AQUI está a correção principal:
# Em vez de esperar que o Flask passe data_str por kwargs, nós lemos do request.form e chamamos uma função validada.
@app.post("/adicionar")
@log_acao("Adicionar despesa")
def adicionar():
    try:
        return _adicionar_validado(
            data_str=request.form.get("data_str", ""),
            descricao=request.form.get("descricao", ""),
            categoria=request.form.get("categoria", ""),
            valor_str=request.form.get("valor_str", ""),
        )
    except ValueError as e:
        flash(str(e), "warn")
        return redirect(url_for("index"))


@validar_despesa
def _adicionar_validado(*, data_str: str, descricao: str, categoria: str, valor_str: str,
                        data_obj, valor):
    df = ler_df()

    despesa = Despesa(
        data=data_obj,
        descricao=descricao,
        categoria=categoria,
        valor=valor
    )

    df = pd.concat([df, pd.DataFrame([despesa.as_dict()])], ignore_index=True)
    guardar_df(df)

    flash("Despesa adicionada com sucesso ✅", "ok")
    return redirect(url_for("index"))


@app.get("/resumo")
def resumo():
    df = ler_df()
    if df.empty:
        return render_template(
            "resumo.html",
            categorias=CATEGORIAS_PADRAO,
            resumo={"total": 0, "media": 0, "desvio": 0, "count": 0},
            por_categoria=[],
        )

    valores = df["valor"].to_numpy(dtype=float)

    resumo_stats = {
        "total": float(np.sum(valores)),
        "media": float(np.mean(valores)),
        "desvio": float(np.std(valores)),
        "count": int(len(valores)),
    }

    agrupado = (
        df.groupby("categoria")["valor"]
        .sum()
        .reset_index()
        .sort_values(by="valor", ascending=False)
    )

    por_categoria = agrupado.to_dict(orient="records")

    return render_template(
        "resumo.html",
        categorias=CATEGORIAS_PADRAO,
        resumo=resumo_stats,
        por_categoria=por_categoria,
    )


@app.post("/limpar")
@log_acao("Limpar dados")
def limpar():
    df = pd.DataFrame(columns=["data", "descricao", "categoria", "valor"])
    guardar_df(df)
    flash("Dados limpos. Começo novo: folha em branco 🧾", "warn")
    return redirect(url_for("index"))


if __name__ == "__main__":
    garantir_csv()
    # Evita reinícios que às vezes atrapalham no Windows/VSCode
    app.run(debug=True, use_reloader=False)
