import streamlit as st
import json
from backend import criar_exemplo_squad, adicionar_exemplo

# Estado persistente
if "dataset_total" not in st.session_state:
    st.session_state.dataset_total = {"data": []}

st.title("Gerador de Dataset SQuAD")

st.subheader("Adicionar novo exemplo")

contexto = st.text_area("Contexto", height=150)
pergunta = st.text_input("Pergunta")
resposta = st.text_input("Resposta (deixe vazio se não houver)")

# Contagem de palavras do contexto
quantidade_palavras = len(contexto.split())

col1, col2 = st.columns(2)

with col1:
    if st.button("Adicionar Pergunta"):

        # Verifica campos vazios
        if not contexto or not pergunta:
            st.warning("Preencha contexto e pergunta!")

        # Verifica limite de palavras
        elif quantidade_palavras > 350:
            st.error(
                f"O contexto possui {quantidade_palavras} palavras. "
                "O limite é 350 palavras."
            )

        # Verifica se a pergunta termina com ?
        elif not pergunta.strip().endswith("?"):
            st.error("A pergunta deve terminar com '?'")

        else:
            try:
                exemplo = criar_exemplo_squad(
                    contexto,
                    pergunta,
                    resposta
                )

                adicionar_exemplo(
                    st.session_state.dataset_total,
                    exemplo
                )

                st.success("Exemplo adicionado!")

            except ValueError as e:
                st.error(str(e))

with col2:
    if st.button("Limpar dataset"):
        st.session_state.dataset_total = {"data": []}
        st.success("Dataset limpo!")

st.divider()

st.subheader("Preview do Dataset")
st.json(st.session_state.dataset_total)

st.write(
    f"Total de exemplos: "
    f"{len(st.session_state.dataset_total['data'])}"
)

st.write(f"Palavras no contexto: {quantidade_palavras}/350")

st.divider()

st.subheader("Exportar")

json_str = json.dumps(
    st.session_state.dataset_total,
    indent=2,
    ensure_ascii=False
)

st.download_button(
    label="Baixar dataset_squad.json",
    data=json_str,
    file_name="dataset_squad.json",
    mime="application/json"
)