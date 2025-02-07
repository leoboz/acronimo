import streamlit as st
from collections import defaultdict

@st.cache_resource
def get_shared_state():
    return {
        "word": "",
        "suggestions": defaultdict(list),
        "votes": defaultdict(dict),
        "results": {},
        "scores": defaultdict(int)  # Mantém pontuação dos usuários
    }

shared_state = get_shared_state()

st.set_page_config(page_title="Acrônimo Interativo", layout="centered")
st.title("📱 Acrônimo Interativo")

if not shared_state["word"]:
    shared_state["word"] = st.text_input("Escolha uma palavra base:", placeholder="Digite aqui e pressione Enter").strip().upper()

st.write(f"🔤 Palavra base: **{shared_state['word']}**")

if shared_state["word"]:
    letters = list(shared_state["word"])
    
    st.subheader("✍️ Sugira palavras para cada letra")
    user_name = st.text_input("👤 Seu nome:", placeholder="Digite seu nome e pressione Enter", key="user_name")
    
    if user_name:
        for letter in letters:
            suggestion = st.text_input(f"🔠 Palavra para '{letter}':", placeholder=f"Digite para '{letter}' e pressione Enter", key=f"suggestion_{letter}")
            if suggestion:
                shared_state["suggestions"][letter].append((suggestion, user_name))
                if suggestion not in shared_state["votes"][letter]:
                    shared_state["votes"][letter][suggestion] = 0
                st.experimental_rerun()
    
    st.subheader("👍 Vote nas sugestões")
    for letter, words in shared_state["suggestions"].items():
        if words:
            word_options = [w[0] for w in words]  # Extrai apenas as palavras
            choice = st.radio(f"Escolha a melhor palavra para '{letter}':", word_options, key=f"vote_{letter}", horizontal=True)
            if st.button(f"Votar '{letter}'", key=f"vote_btn_{letter}"):
                shared_state["votes"][letter][choice] += 1
                st.experimental_rerun()
    
    # Exibir acrônimo vencedor apenas quando houver votos
    st.subheader("🏆 Acrônimo Atual")
    shared_state["results"] = {
        l: max(w.keys(), key=lambda x: w[x]) if w and any(v > 0 for v in w.values()) else "?"
        for l, w in shared_state["votes"].items()
    }
    st.markdown(f"**{' '.join(shared_state['results'].values())}**")
    
    # Atualiza pontuação dos usuários corretamente
    shared_state["scores"] = defaultdict(int)  # Reset para evitar duplicação
    for letter, word in shared_state["results"].items():
        if word != "?":  # Só conta pontos para palavras vencedoras
            for suggestion, user in shared_state["suggestions"][letter]:
                if suggestion == word:
                    shared_state["scores"][user] += 10  # Cada palavra vencedora dá 10 pontos
    
    st.subheader("🥇 Ranking de Pontuação")
    sorted_scores = sorted(shared_state["scores"].items(), key=lambda x: x[1], reverse=True)
    for user, score in sorted_scores:
        st.write(f"🏅 **{user}**: {score} pontos")
    
    # Botão para resetar tudo
    if st.button("🔄 Resetar Jogo", key="reset"):
        shared_state.clear()
        st.experimental_rerun()
