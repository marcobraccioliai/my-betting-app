import streamlit as st

st.set_page_config(page_title="Parser Cavalli", layout="centered")

st.markdown("""
    <style>
    /* 1. Sfondo rosso porpora solo per l'area principale */
    [data-testid="stAppViewContainer"] {
        background-color: #B20000 !important;
    }

    /* 2. Testo crema solo per l'area principale (target ultra-specifico) */
    .stApp div[data-testid="stMarkdownContainer"], 
    .stApp label, 
    .stApp h1, .stApp h2, .stApp h3 {
        color: #FFFDD0 !important;
    }

    /* 3. Reset totale e forzato della sidebar */
    [data-testid="stSidebar"] {
        background-color: #F0F2F6 !important;
    }
    
    /* Forza il testo della sidebar a nero, ignorando qualsiasi regola precedente */
    [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p {
        color: #000000 !important;
    }

    /* 4. Pulsanti */
    .stButton button {
        color: #000000 !important;
        background-color: #FFFDD0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ Converter Quote Singoli Cavalli")
st.write("Incolla qui sotto il testo grezzo copiato dal sito SNAI (quote cavallo vincente, al totalizzatore):")

raw_text = st.text_area("Incolla testo grezzo:", height=200)

if st.button("🚀🚀🚀🚀"):
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
