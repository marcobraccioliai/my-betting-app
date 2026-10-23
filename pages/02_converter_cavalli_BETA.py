import streamlit as st

st.set_page_config(page_title="Parser Cavalli", layout="centered")
st.title("✂️ Converter Quote Singoli Cavalli")

raw_text = st.text_area("Incolla testo grezzo:")

if st.button("Converti"):
    try:
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        result = []
        current_horse = None
        
        for line in lines:
            if line.isdigit():
                current_horse = line
            if "Vincente" in line and current_horse:
                quota = line.replace("Vincente", "").strip()
                result.append(f"{current_horse}:{quota}")
                current_horse = None
        
        if result:
            st.code(", ".join(result))
        else:
            st.error("Nessun dato estratto.")
    except Exception as e:
        st.error(f"Errore: {e}")
