import streamlit as st
from collections import defaultdict

# Inicializa o estado da sessão
if "word" not in st.session_state:
    st.session_state.word = ""
    st.session_state.suggestions = defaultdict(list)
    st.session_state.votes = defaultdict(dict)
    st.session_state.results = {}

st.title("Acrônimo Interativo")

# Define a palavra base do acrônimo
st.session_state.word = st.text_input("Escolha uma palavra base:", st.session_state.word).strip().upper()

if st.session_state.word:
    letters = list(st.session_state.word)
    
    st.subheader("Sugira palavras para cada letra")
    for letter in letters:
        suggestion = st.text_input(f"Palavra para '{letter}':", key=f"suggestion_{letter}")
        if st.button(f"Enviar '{letter}'") and suggestion:
            st.session_state.suggestions[letter].append(suggestion)
            st.session_state.votes[letter][suggestion] = 0

    st.subheader("Vote nas sugestões")
    for letter, words in st.session_state.suggestions.items():
        if words:
            choice = st.radio(f"Escolha a melhor palavra para '{letter}':", words, key=f"vote_{letter}")
            if st.button(f"Votar '{letter}'"):
                st.session_state.votes[letter][choice] += 1
    
    # Exibir acrônimo vencedor em tempo real
    st.subheader("Acrônimo Atual")
    st.session_state.results = {l: max(w.keys(), key=lambda x: w[x]) if w else "?" for l, w in st.session_state.votes.items()}
    st.write(" ".join(st.session_state.results.values()))
    
    # Botão para resetar tudo
    if st.button("Resetar Jogo"):
        st.session_state.word = ""
        st.session_state.suggestions = defaultdict(list)
        st.session_state.votes = defaultdict(dict)
        st.session_state.results = {}
        st.experimental_rerun()
