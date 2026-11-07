import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="HyppoBingo BETA", layout="centered")

# --- CSS PER SFONDO ROSSO E TESTO LEGGIBILE ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #B20000 !important; }
    .stApp div[data-testid="stMarkdownContainer"], .stApp label, .stApp h1, .stApp h2, .stApp h3 { color: #FFFDD0 !important; }
    [data-testid="stSidebar"] { background-color: #F0F2F6 !important; }
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p { color: #000000 !important; }
    .stButton button { color: #000000 !important; background-color: #FFFDD0 !important; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    budget = st.number_input("Budget Totale (€)", value=200.0)
    max_puntata = st.number_input("Limite Singola Puntata (€)", value=10.0)
    frazione_kelly = st.slider("Prudenza (Frazione Kelly)", 0.1, 1.0, 0.5)

st.title("🏇 HyppoBingo BETA")

input_cavalli = st.text_area("1. Incolla Dati Cavalli:", height=150)
input_coppie = st.text_input("2. Incolla Accoppiate:", "")

if st.button("🚀 CALCOLA"):
    try:
        # PARSING CAVALLI (Logica V1 mantenuta)
        lines = [i.strip() for i in input_cavalli.replace('\n', ',').split(',') if i.strip()]
        data_cavalli = {'numero': [], 'quota_vincente': []}
        for item in lines:
            if ':' in item:
                n, q = item.split(':')
                data_cavalli['numero'].append(int(n))
                data_cavalli['quota_vincente'].append(float(q))
        
        df = pd.DataFrame(data_cavalli)
        
        # CALCOLO PROBABILITÀ (Logica V1 mantenuta)
        prob = 1 / df['quota_vincente']
        df['prob_mercato'] = prob / prob.sum()
        
        # Simulazione Monte Carlo (Logica V1 mantenuta)
        n_sim = 100000
        conteggi = {c.split(':')[0]: 0 for c in input_coppie.split(",") if ":" in c}
        rng = np.random.default_rng()
        
        probs_norm = df['prob_mercato'].values
        # Ripristino somma a 1 stretta per evitare crash di numpy
        probs_norm /= probs_norm.sum()
        
        for _ in range(n_sim):
            podio = rng.choice(df['numero'], size=3, replace=False, p=probs_norm)
            for c_str in conteggi:
                c1, c2 = map(int, c_str.split("-"))
                if c1 in podio and c2 in podio: conteggi[c_str] += 1
        
        # RISULTATI (Grafica corretta per visibilità)
        st.subheader("💰 Verdetto dello Sportello")
        for c_str, vinte in conteggi.items():
            prob = vinte / n_sim
            quota = float(input_coppie.split(c_str+":")[1].split(",")[0])
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
                
    except Exception as e: st.error(f"Errore nel calcolo: {e}")
