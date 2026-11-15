import streamlit as st

st.set_page_config(page_title="Parser Cavalli", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #B20000 !important; }
    .stApp div[data-testid="stMarkdownContainer"], .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: #FFFDD0 !important; }
    [data-testid="stSidebar"] { background-color: #F0F2F6 !important; }
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p { color: #000000 !important; }
    .stButton button { color: #000000 !important; background-color: #FFFDD0 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ Converter Quote Singoli Cavalli")
raw_text = st.text_area("Incolla testo grezzo:", height=200)

if st.button("🚀🚀🚀🚀"):
    try:
        # Pulizia base: teniamo solo linee non vuote
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        result = []
        
        # Logica: Cerchiamo blocchi coerenti
        # Un cavallo è identificato da "N" (numero) seguito da blocchi di info
        # e infine da "Vincente/V" + Quota.
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Se la riga è un numero (potenziale cavallo)
            if line.isdigit() and len(line) < 3: 
                num_cavallo = line
                # Cerchiamo la quota nelle prossime 5 righe
                for j in range(i + 1, min(i + 8, len(lines))):
                    if "Vincente" in lines[j] or (lines[j].strip() == "V" and j+1 < len(lines)):
                        # Gestione PC (Vincente 9.00) o Mobile (V -> riga dopo 9.00)
                        raw_quota = lines[j+1] if lines[j].strip() == "V" else lines[j].replace("Vincente", "")
                        
                        try:
                            quota = float(raw_quota.strip())
                            if quota <= 1.0: quota = 1000.0
                            result.append(f"{num_cavallo}:{quota:.2f}")
                            i = j # Saltiamo avanti
                            break
                        except:
                            pass
            i += 1
        
        if result:
            st.code(", ".join(result))
        else:
            st.error("Nessun dato estratto. Formato non riconosciuto.")
    except Exception as e:
        st.error(f"Errore: {e}")
