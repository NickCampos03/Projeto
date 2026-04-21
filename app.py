import streamlit as st
import json
from backend import criar_exemplo_squad, adicionar_exemplo

# Estado persistente
if "dataset_total" not in st.session_state:
    st.session_state.dataset_total = {"data": []}

st.title("🧠 Gerador de Dataset SQuAD")

st.subheader("Adicionar novo exemplo")

contexto = st.text_area("Contexto", height=150)
pergunta = st.text_input("Pergunta")
resposta = st.text_input("Resposta (deixe vazio se não houver)")

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Adicionar exemplo"):
        if not contexto or not pergunta:
            st.warning("Preencha contexto e pergunta!")
        else:
            try:
                exemplo = criar_exemplo_squad(contexto, pergunta, resposta)
                adicionar_exemplo(st.session_state.dataset_total, exemplo)
                st.success("Exemplo adicionado!")
            except ValueError as e:
                st.error(str(e))

with col2:
    if st.button("🗑️ Limpar dataset"):
        st.session_state.dataset_total = {"data": []}
        st.success("Dataset limpo!")

st.divider()

st.subheader("📊 Preview do Dataset")
st.json(st.session_state.dataset_total)

st.write(f"Total de exemplos: {len(st.session_state.dataset_total['data'])}")

st.divider()

st.subheader("💾 Exportar")

json_str = json.dumps(
    st.session_state.dataset_total,
    indent=2,
    ensure_ascii=False
)

st.download_button(
    label="⬇️ Baixar dataset_squad.json",
    data=json_str,
    file_name="dataset_squad.json",
    mime="application/json"
)