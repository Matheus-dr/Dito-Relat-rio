import pandas as pd
import streamlit as st
from io import BytesIO

st.title("Relatório One Up • DITO")

uploaded = st.file_uploader("Envie o CSV exportado da DITO", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    # Seleciona apenas as colunas necessárias
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

    # Ajusta percentual
    df["% REALIZADOS"] = df["% REALIZADOS"] / 100

    # Ordena
    df = df.sort_values(["FILIAL", "VENDEDORA"])

    st.subheader("Prévia do relatório")
    st.dataframe(df)

    # Gera Excel em memória
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Resumo Geral")
        for filial, sub in df.groupby("FILIAL"):
            sub.to_excel(writer, index=False, sheet_name=str(filial)[:31])

    st.download_button(
        "Baixar Excel final",
        data=output.getvalue(),
        file_name="relatorio_one_up.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
