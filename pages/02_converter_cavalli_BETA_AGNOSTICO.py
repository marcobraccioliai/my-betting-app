import streamlit as st

st.set_page_config(page_title="Parser Cavalli", layout="centered")

st.markdown("""
    <style>
    /* Sfondo rosso porpora solo per l'area principale */
    [data-testid="stAppViewContainer"] {
        background-color: #B20000 !important;
    }
    /* Testo crema solo per l'area principale */
    .stApp div[data-testid="stMarkdownContainer"], 
    .stApp label, .stApp h1, .stApp h2, .stApp h3 {
        color: #FFFDD0 !important;
    }
    /* Pulsanti */
    .stButton button {
        color: #000000 !important;
        background-color: #FFFDD0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ Converter Quote Singoli Cavalli")
raw_text = st.text_area("Incolla testo grezzo:", height=200)

if st.button("🚀🚀🚀🚀"):
    try:
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        result = []
        
        # Itero per trovare coppie (Numero Cavallo, Quota)
        # Cerco ogni riga che sia un numero intero (candidato cavallo)
        # e la quota associata "V" o "Vincente" nelle 3 righe successive
        for i in range(len(lines)):
            if lines[i].isdigit() and len(lines[i]) < 3:
                num_cavallo = lines[i]
                for j in range(i + 1, min(i + 4, len(lines))):
                    line_j = lines[j].upper()
                    if ("V" in line_j) and any(c.isdigit() for c in line_j):
                        # Estrazione numero da stringa tipo "V 3.25" o "Vincente 3.00"
                        valori = [float(s) for s in line_j.replace('V', '').replace('INCENTE', '').replace('INTE', '').split() if s.replace('.','',1).isdigit()]
                        if valori:
                            quota = valori[0]
                            if quota <= 1.0: quota = 1000.0
                            result.append(f"{num_cavallo}:{quota:.2f}")
                            break
        
        if result:
            st.code(", ".join(result))
        else:
            st.error("Nessun dato estratto.")
    except Exception as e:
        st.error(f"Errore: {e}")
