import streamlit as st
from collections import defaultdict

@st.cache_resource
def get_shared_state():
    return {
        "word": "",
        "suggestions": defaultdict(list),
        "votes": defaultdict(dict),
        "results": {}
    }

shared_state = get_shared_state()

st.title("Acrônimo Interativo")

if not shared_state["word"]:
    shared_state["word"] = st.text_input("Escolha uma palavra base:").strip().upper()

st.write(f"Palavra base: {shared_state['word']}")

if shared_state["word"]:
    letters = list(shared_state["word"])
    
    st.subheader("Sugira palavras para cada letra")
    for letter in letters:
        suggestion = st.text_input(f"Palavra para '{letter}':", key=f"suggestion_{letter}")
        if st.button(f"Enviar '{letter}'") and suggestion:
            shared_state["suggestions"][letter].append(suggestion)
            shared_state["votes"][letter][suggestion] = 0

    st.subheader("Vote nas sugestões")
    for letter, words in shared_state["suggestions"].items():
        if words:
            choice = st.radio(f"Escolha a melhor palavra para '{letter}':", words, key=f"vote_{letter}")
            if st.button(f"Votar '{letter}'"):
                shared_state["votes"][letter][choice] += 1
    
    # Exibir acrônimo vencedor em tempo real
    st.subheader("Acrônimo Atual")
    shared_state["results"] = {l: max(w.keys(), key=lambda x: w[x]) if w else "?" for l, w in shared_state["votes"].items()}
    st.write(" ".join(shared_state["results"].values()))
    
    # Botão para resetar tudo
    if st.button("Resetar Jogo"):
        shared_state["word"] = ""
        shared_state["suggestions"] = defaultdict(list)
        shared_state["votes"] = defaultdict(dict)
        shared_state["results"] = {}
        st.experimental_rerun()
