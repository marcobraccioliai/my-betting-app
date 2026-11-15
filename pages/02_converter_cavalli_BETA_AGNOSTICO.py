import streamlit as st
import re

st.set_page_config(page_title="Parser Cavalli", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #B20000 !important; }
    .stApp div[data-testid="stMarkdownContainer"], .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: #FFFDD0 !important; }
    .stButton button { color: #000000 !important; background-color: #FFFDD0 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ Converter Quote Singoli Cavalli")
raw_text = st.text_area("Incolla testo grezzo:", height=200)

if st.button("🚀🚀🚀🚀"):
    try:
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        result = []
        current_horse = None
        
        # Regex per trovare un numero con decimale (es. 9.00)
        quota_pattern = re.compile(r'\d+\.\d{2}')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # 1. Identifica il cavallo (linea con solo numero, escludendo posizioni arrivo tipo "1°")
            if line.isdigit() and len(line) < 3:
                current_horse = line
            
            # 2. Se abbiamo un cavallo, cerchiamo la quota nelle righe vicine
            if current_horse:
                # Verifica se la riga contiene "V" o "Vincente"
                if "V" in line.upper() or "VINCENTE" in line.upper():
                    # Guarda questa riga e le 2 successive per un numero decimale
                    found_quota = None
                    for j in range(i, min(i + 3, len(lines))):
                        match = quota_pattern.search(lines[j])
                        if match:
                            found_quota = match.group()
                            break
                    
                    if found_quota:
                        q = float(found_quota)
                        if q <= 1.0: q = 1000.0
                        result.append(f"{current_horse}:{q:.2f}")
                        current_horse = None # Reset
            i += 1
            
        if result:
            st.code(", ".join(result))
        else:
            st.error("Nessun dato estratto. Formato non riconosciuto.")
    except Exception as e:
        st.error(f"Errore tecnico: {e}")
