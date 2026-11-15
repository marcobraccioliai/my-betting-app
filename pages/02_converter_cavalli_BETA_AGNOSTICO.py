import streamlit as st

st.set_page_config(page_title="Parser Cavalli", layout="centered")

st.markdown("""
    <style>
    /* 1. Sfondo rosso porpora */
    [data-testid="stAppViewContainer"] { background-color: #B20000 !important; }

    /* 2. Testo crema */
    .stApp div[data-testid="stMarkdownContainer"], 
    .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: #FFFDD0 !important; }

    /* 3. Sidebar */
    [data-testid="stSidebar"] { background-color: #F0F2F6 !important; }
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p { color: #000000 !important; }

    /* 4. Pulsanti */
    .stButton button { color: #000000 !important; background-color: #FFFDD0 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ Converter Quote Singoli Cavalli")
st.write("Incolla qui sotto il testo grezzo (PC, Tablet o Smartphone):")

raw_text = st.text_area("Incolla testo grezzo:", height=200)

if st.button("🚀🚀🚀🚀"):
    try:
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        result = []
        current_horse = None
        
        for i, line in enumerate(lines):
            # 1. Identifica il numero del cavallo
            if line.isdigit():
                current_horse = line
                continue
            
            # 2. Cerca la quota (gestisce sia "Vincente 9.00" che "V 9.00")
            is_header = line.lower().startswith("vincente") or line.strip().upper() == "V"
            
            if current_horse and is_header:
                # Se la quota è nella stessa riga
                parts = line.split()
                quota = None
                
                # Prova a prendere l'ultimo elemento della riga
                try:
                    quota = float(parts[-1])
                except:
                    # Se non è nella stessa riga, guarda la riga successiva
                    if i + 1 < len(lines):
                        try:
                            quota = float(lines[i+1].strip())
                        except:
                            pass
                
                if quota:
                    if quota <= 1.0:
                        quota = 1000.0
                    result.append(f"{current_horse}:{quota:.2f}")
                    current_horse = None
        
        if result:
            st.code(", ".join(result))
        else:
            st.error("Nessun dato estratto. Verifica il formato.")
    except Exception as e:
        st.error(f"Errore: {e}")
