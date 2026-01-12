import pandas as pd
import streamlit as st
from io import BytesIO

st.title("Relatório One Up • DITO")

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
        st.error("CSV inválido. Faltando colunas: " + ", ".join(sorted(faltando)))
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

    # Ajusta % (de 0-100 para 0-1)
    df["% REALIZADOS"] = (df["% REALIZADOS"] / 100).round(4)

    # Ordena
    df = df.sort_values(["FILIAL", "VENDEDORA"])

    # Mostra na tela
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("Baixar relatório")

    # ===== Download CSV =====
    csv_bytes = df.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig")

    st.download_button(
        label="📥 Baixar CSV",
        data=csv_bytes,
        file_name="relatorio_one_up_dito.csv",
        mime="text/csv",
    )

    # ===== Download Excel =====
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Relatório")
    output.seek(0)

    st.download_button(
        label="📥 Baixar Excel",
        data=output,
        file_name="relatorio_one_up_dito.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
