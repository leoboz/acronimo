import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="Acrónimo Interactivo", layout="centered")

@st.cache_resource
def get_shared_state():
    return {
        "word": "",
        "suggestions": defaultdict(list),
        "votes": defaultdict(dict),
        "results": {},
        "scores": defaultdict(int)  # Mantiene la puntuación de los usuarios
    }

shared_state = get_shared_state()

st.title("📱 Acrónimo Interactivo")

if "reset" in st.session_state and st.session_state["reset"]:
    shared_state["word"] = ""
    shared_state["suggestions"] = defaultdict(list)
    shared_state["votes"] = defaultdict(dict)
    shared_state["results"] = {}
    shared_state["scores"] = defaultdict(int)
    st.session_state["reset"] = False
    st.rerun()

if not shared_state["word"]:
    shared_state["word"] = st.text_input("Elige una palabra base:", placeholder="Escribe aquí y presiona Enter").strip().upper()

st.write(f"🔤 Palabra base: **{shared_state['word']}**")

if shared_state["word"]:
    letters = list(shared_state["word"])
    
    st.subheader("✍️ Sugiere palabras para cada letra")
    user_name = st.text_input("👤 Tu nombre:", placeholder="Escribe tu nombre y presiona Enter", key="user_name")
    
    if user_name:
        for letter in letters:
            suggestion = st.text_input(f"🔠 Palabra para '{letter}':", placeholder=f"Escribe para '{letter}' y presiona Enter", key=f"suggestion_{letter}")
            if suggestion:
                shared_state["suggestions"][letter].append((suggestion, user_name))
                if suggestion not in shared_state["votes"][letter]:
                    shared_state["votes"][letter][suggestion] = 0
                st.rerun()
    
    st.subheader("👍 Vota por las sugerencias")
    for letter, words in shared_state["suggestions"].items():
        if words:
            word_options = list(set(w[0] for w in words))  # Extrae solo las palabras únicas
            choice = st.radio(f"Elige la mejor palabra para '{letter}':", word_options, key=f"vote_{letter}", horizontal=True)
            if st.button(f"Votar '{letter}'", key=f"vote_btn_{letter}"):
                shared_state["votes"][letter][choice] += 1
                st.rerun()
    
    # Mostrar acrónimo ganador solo cuando haya votos
    st.subheader("🏆 Acrónimo Actual")
    shared_state["results"] = {
        l: max(w.keys(), key=lambda x: w[x]) if w and any(v > 0 for v in w.values()) else "?"
        for l, w in shared_state["votes"].items()
    }
    st.markdown(f"**{' '.join(shared_state['results'].values())}**")
    
    # Actualizar puntuación de los usuarios correctamente
    for letter, word in shared_state["results"].items():
        if word != "?":  # Solo cuenta puntos para palabras ganadoras
            for suggestion, user in shared_state["suggestions"][letter]:
                if suggestion == word:
                    shared_state["scores"][user] += 10  # Cada palabra ganadora da 10 puntos
    
    st.subheader("🥇 Ranking de Puntuación")
    sorted_scores = sorted(shared_state["scores"].items(), key=lambda x: x[1], reverse=True)
    for user, score in sorted_scores:
        st.write(f"🏅 **{user}**: {score} puntos")
    
    # Botón para reiniciar todo
    if st.button("🔄 Reiniciar Juego", key="reset"):
        st.session_state["reset"] = True
        st.rerun()
