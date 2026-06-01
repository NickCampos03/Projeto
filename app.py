import streamlit as st
import json
import tempfile
import os

from backend import (
    criar_exemplo_squad,
    adicionar_exemplo,
    fazer_merge_squad
)

# ==========================
# ESTADO
# ==========================

if "dataset_total" not in st.session_state:
    st.session_state.dataset_total = {
        "version": "v2.0",
        "data": []
    }

# ==========================
# TÍTULO
# ==========================

st.title("Gerador de Dataset SQuAD 2.0")

# ==========================
# CRIAÇÃO DE EXEMPLOS
# ==========================

st.header("Criar Dataset")

contexto = st.text_area(
    "Contexto",
    height=180
)

pergunta = st.text_input(
    "Pergunta"
)

is_impossible = st.checkbox(
    "Pergunta impossível"
)

if is_impossible:

    resposta = ""

    resposta_plausivel = st.text_input(
        "Resposta plausível (opcional)"
    )

else:

    resposta = st.text_input(
        "Resposta"
    )

    resposta_plausivel = ""

quantidade_palavras = len(contexto.split())

col1, col2 = st.columns(2)

with col1:

    if st.button("Adicionar Pergunta"):

        if not contexto:
            st.warning("Informe um contexto.")

        elif not pergunta:
            st.warning("Informe uma pergunta.")

        elif quantidade_palavras > 350:
            st.error(
                f"Contexto possui {quantidade_palavras} palavras. "
                "Limite: 350."
            )

        elif not pergunta.strip().endswith("?"):
            st.error(
                "A pergunta deve terminar com '?'"
            )

        else:

            try:

                exemplo = criar_exemplo_squad(
                    contexto=contexto,
                    pergunta=pergunta,
                    resposta=resposta,
                    resposta_plausivel=resposta_plausivel
                )

                adicionar_exemplo(
                    st.session_state.dataset_total,
                    exemplo
                )

                st.success(
                    "Pergunta adicionada."
                )

            except ValueError as e:
                st.error(str(e))

with col2:

    if st.button("Limpar Dataset"):

        st.session_state.dataset_total = {
            "version": "v2.0",
            "data": []
        }

        st.success("Dataset limpo.")

# ==========================
# PREVIEW
# ==========================

st.divider()

st.header("Preview")

st.json(
    st.session_state.dataset_total
)

total_contextos = len(
    st.session_state.dataset_total["data"]
)

total_perguntas = 0

for contexto_item in st.session_state.dataset_total["data"]:

    total_perguntas += len(
        contexto_item["qas"]
    )

st.write(
    f"Contextos: {total_contextos}"
)

st.write(
    f"Perguntas: {total_perguntas}"
)

st.write(
    f"Palavras no contexto atual: "
    f"{quantidade_palavras}/350"
)

# ==========================
# EXPORTAR
# ==========================

st.divider()

st.header("Exportar Dataset")

json_str = json.dumps(
    st.session_state.dataset_total,
    ensure_ascii=False,
    indent=2
)

st.download_button(
    label="Baixar dataset_squad.json",
    data=json_str,
    file_name="dataset_squad.json",
    mime="application/json"
)

# ==========================
# MERGE
# ==========================

st.divider()

st.header("Merge de Datasets")

arquivo_base = st.file_uploader(
    "Dataset Principal",
    type=["json"],
    key="base"
)

arquivo_novo = st.file_uploader(
    "Dataset para Mesclar",
    type=["json"],
    key="novo"
)

if st.button("Executar Merge"):

    if not arquivo_base or not arquivo_novo:

        st.warning(
            "Envie os dois arquivos."
        )

    else:

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".json"
            ) as f1:

                f1.write(
                    arquivo_base.getvalue()
                )

                caminho_base = f1.name

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".json"
            ) as f2:

                f2.write(
                    arquivo_novo.getvalue()
                )

                caminho_novo = f2.name

            caminho_saida = tempfile.mktemp(
                suffix=".json"
            )

            fazer_merge_squad(
                caminho_base,
                caminho_novo,
                caminho_saida
            )

            with open(
                caminho_saida,
                "r",
                encoding="utf-8"
            ) as f:

                resultado_merge = f.read()

            st.success(
                "Merge concluído."
            )

            st.download_button(
                "Baixar Dataset Mesclado",
                resultado_merge,
                file_name="dataset_merged.json",
                mime="application/json"
            )

            os.remove(caminho_base)
            os.remove(caminho_novo)
            os.remove(caminho_saida)

        except Exception as e:

            st.error(
                f"Erro no merge: {e}"
            )