import pandas as pd
import streamlit as st
from io import BytesIO

st.title("Relatório One Up • DITO")

uploaded = st.file_uploader("Envie o CSV exportado da DITO", type=["csv"])

uploaded = st.file_uploader("Envie o CSV exportado da DITO", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    colunas_necessarias = {
        "nome_loja",
        "nome_vendedor",
        "contatos_disponibilizados",
        "contatos_realizados",
        "contatos_realizados_porcentagem",
    }

    faltando = colunas_necessarias - set(df.columns)

    if faltando:
        st.error(
            "CSV inválido. Faltando colunas: "
            + ", ".join(sorted(faltando))
        )
        st.stop()

    # Seleciona só o que interessa
    df = df[
        [
            "nome_loja",
            "nome_vendedor",
            "contatos_disponibilizados",
            "contatos_realizados",
            "contatos_realizados_porcentagem",
        ]
    ].copy()

    # Renomeia colunas
    df.columns = [
        "FILIAL",
        "VENDEDORA",
        "CONTATOS DISPONIBILIZADOS",
        "CONTATOS REALIZADOS",
        "% REALIZADOS",
    ]

    df["% REALIZADOS"] = (df["% REALIZADOS"] / 100).round(4)

    df = df.sort_values(["FILIAL", "VENDEDORA"])
