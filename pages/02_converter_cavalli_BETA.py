import streamlit as st

st.markdown("""
    <style>
    /* 1. Sfondo rosso porpora solo per l'area principale */
    [data-testid="stAppViewContainer"] {
        background-color: #B20000 !important;
    }

    /* 2. Testo crema solo per i contenuti dentro l'area principale */
    [data-testid="stAppViewContainer"] h1, 
    [data-testid="stAppViewContainer"] h2, 
    [data-testid="stAppViewContainer"] h3, 
    [data-testid="stAppViewContainer"] p, 
    [data-testid="stAppViewContainer"] div:not([data-testid="stSidebar"]), 
    [data-testid="stAppViewContainer"] label {
        color: #FFFDD0 !important;
    }

    /* 3. Forza la Sidebar al suo stile nativo (il contrario del CSS globale) */
    [data-testid="stSidebar"] {
        background-color: #F0F2F6 !important;
        color: #31333F !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #31333F !important;
    }

    /* 4. Forza il testo del bottone a nero */
    .stButton button {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Parser Cavalli", layout="centered")
st.title("✂️ Converter Quote Singoli Cavalli")
st.write("Incolla qui sotto il testo grezzo copiato dal sito SNAI (quote cavallo vincente, al totalizzatore):")

raw_text = st.text_area("Incolla testo grezzo:", height=200)

if st.button("Converti in stringa"):
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
