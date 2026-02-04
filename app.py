from __future__ import annotations

import os
from datetime import date

import numpy as np
import pandas as pd
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
)

from models import Despesa
from utils import CATEGORIAS_PADRAO, log_acao, validar_despesa

app = Flask(__name__)
app.secret_key = "iefp-segredo-simples"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "despesas.csv")


# -----------------------------
# Helpers de ficheiro / pandas
# -----------------------------
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

    # Lê o CSV
    df = pd.read_csv(CSV_PATH)

    # Garante colunas mesmo se o ficheiro vier “estranho”
    colunas = ["data", "descricao", "categoria", "valor"]
    for c in colunas:
        if c not in df.columns:
            df[c] = "" if c != "valor" else 0.0
    df = df[colunas]

    # Normaliza tipos
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
        df["descricao"] = df["descricao"].astype(str).fillna("")
        df["categoria"] = df["categoria"].astype(str).fillna("")
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0.0)

        # Remove linhas com data inválida (coerce -> NaT -> NaN)
        df = df[df["data"].notna()]

    return df


def guardar_df(df: pd.DataFrame) -> None:
    df.to_csv(CSV_PATH, index=False)


# -----------------------------
# Rotas
# -----------------------------
@app.get("/")
def index():
    df = ler_df()

    # filtro por categoria
    categoria_filtro = request.args.get("categoria", "").strip()
    if categoria_filtro:
        df = df[df["categoria"] == categoria_filtro]

    # ordenar por data desc
    if not df.empty:
        df = df.sort_values(by="data", ascending=False)

    despesas = df.to_dict(orient="records")

    # ✅ Resumo do mês atual (mais apelativo)
    hoje = date.today()
    total_mes = 0.0
    if not df.empty:
        datas = pd.to_datetime(df["data"], errors="coerce")
        mask = (datas.dt.month == hoje.month) & (datas.dt.year == hoje.year)
        total_mes = float(df.loc[mask, "valor"].sum())

    return render_template(
        "index.html",
        despesas=despesas,
        categorias=CATEGORIAS_PADRAO,
        categoria_filtro=categoria_filtro,
        hoje=hoje.isoformat(),
        total_mes=total_mes,
        mes_atual=hoje.month,
        ano_atual=hoje.year,
    )


@app.post("/adicionar")
@log_acao("Adicionar despesa")
def adicionar():
    try:
        # Passa explicitamente os campos do formulário
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
def _adicionar_validado(
    *,
    data_str: str,
    descricao: str,
    categoria: str,
    valor_str: str,
    data_obj,
    valor,
):
    df = ler_df()

    # ✅ Anti-duplicados (mesma data + descrição + valor)
    if not df.empty:
        duplicado = (
            (df["data"].astype(str) == str(data_obj))
            & (df["descricao"].astype(str).str.strip().str.lower() == descricao.strip().lower())
            & (df["valor"].astype(float) == float(valor))
        ).any()

        if duplicado:
            raise ValueError("Esta despesa já existe (mesma data, descrição e valor).")

    despesa = Despesa(
        data=data_obj,
        descricao=descricao,
        categoria=categoria,
        valor=valor,
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

    # NumPy: total, média, desvio padrão
    resumo_stats = {
        "total": float(np.sum(valores)),
        "media": float(np.mean(valores)),
        "desvio": float(np.std(valores)),
        "count": int(len(valores)),
    }

    # Pandas: total por categoria
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


# ✅ Exportar CSV (download)
@app.get("/exportar")
def exportar():
    garantir_csv()
    return send_file(
        CSV_PATH,
        as_attachment=True,
        download_name="despesas.csv",
    )


if __name__ == "__main__":
    garantir_csv()
    # Evita reinícios automáticos que atrapalham no Windows/VSCode
    app.run(debug=True, use_reloader=False)
