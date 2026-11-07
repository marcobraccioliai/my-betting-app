import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="HyppoBingo BETA", layout="centered")

# --- CSS PER SFONDO ROSSO E TESTO LEGGIBILE ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #B20000 !important; }
    .stApp div[data-testid="stMarkdownContainer"], .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: #FFFDD0 !important; }
    .stButton button { color: #000000 !important; background-color: #FFFDD0 !important; }
    /* Forza visibilità testo dentro text area */
    .stTextArea textarea { background-color: #FFFDD0 !important; color: #000000 !important; }
    .stTextInput input { background-color: #FFFDD0 !important; color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🏇 HyppoBingo BETA")

with st.expander("⚙️ Impostazioni Budget", expanded=False):
    budget = st.number_input("Budget Totale (€)", value=200.0)
    max_puntata = st.number_input("Limite Singola Puntata (€)", value=10.0)
    frazione_kelly = st.slider("Prudenza (Frazione Kelly)", 0.1, 1.0, 0.5)

# --- INPUT A PASTONE ---
st.subheader("1. Incolla Dati Cavalli")
input_cavalli = st.text_area("Formato: 4:2.80", height=150)

st.subheader("2. Incolla Accoppiate")
input_coppie = st.text_input("Formato: 4-10:2.54, 3-7:2.75", "")

# --- MOTORE (LOGICA V1) ---
if st.button("🚀 CALCOLA"):
    try:
        # Parsing Cavalli (Nuovo formato N:Quota)
        lines = [i.strip() for i in input_cavalli.replace('\n', ',').split(',') if i.strip()]
        data_cavalli = {'numero': [], 'quota_vincente': []}
        for item in lines:
            if ':' in item:
                n, q = item.split(':')
                data_cavalli['numero'].append(int(n))
                q_val = float(q)
                data_cavalli['quota_vincente'].append(1000.0 if q_val <= 1.0 else q_val)
        
        df = pd.DataFrame(data_cavalli)
        if df.empty:
            st.error("Nessun cavallo trovato.")
            st.stop()
            
        df['prob_mercato'] = (1/df['quota_vincente'])
        df['prob_mercato'] /= df['prob_mercato'].sum()
        
        # Simulazione Monte Carlo
        n_sim = 100000
        conteggi = {c.split(':')[0]: 0 for c in input_coppie.split(",") if ":" in c}
        rng = np.random.default_rng()
        probs_norm = df['prob_mercato'].values
        probs_norm /= probs_norm.sum()
        
        for _ in range(n_sim):
            podio = rng.choice(df['numero'].values, size=3, replace=False, p=probs_norm)
            for c_str in conteggi:
                c1, c2 = map(int, c_str.split("-"))
                if c1 in podio and c2 in podio: conteggi[c_str] += 1
        
        # Risultati
        st.subheader("💰 Verdetto dello Sportello")
        for c_str, vinte in conteggi.items():
            prob = vinte / n_sim
            try:
                quota = float(input_coppie.split(c_str+":")[1].split(",")[0])
            except: continue
            
            roi = (prob * quota) - 1
            if roi > 0:
                puntata = min(np.floor((roi/(quota-1)) * budget * frazione_kelly), max_puntata)
                if puntata >= 2:
                    st.markdown(f"""
                        <div style="background-color: #FFFDD0; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 2px solid #C5A059;">
                            <p style="color: #000000; font-weight: bold; margin: 0; font-size: 20px;">COPPIA {c_str}</p>
                            <p style="color: #000000; margin: 0; font-size: 18px;">👉 PUNTA: <b>{int(puntata)} €</b></p>
                            <p style="color: #000000; margin: 0;">📈 ROI Stimato: {roi:.1%}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
    except Exception as e: st.error(f"Errore: {e}")
