import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="HyppoBingo BETA", layout="centered")
st.title("🏇 HyppoBingo BETA")

with st.sidebar:
    budget = st.number_input("Budget (€)", value=200.0)
    max_puntata = st.number_input("Max Puntata (€)", value=10.0)
    frazione_kelly = st.slider("Kelly", 0.1, 1.0, 0.5)

# --- INPUT A PASTONE ---
st.subheader("1. Incolla Dati Cavalli")
input_cavalli = st.text_area("Formato: 4 (riga) Vincente 2.80", height=150)

st.subheader("2. Incolla Accoppiate")
input_coppie = st.text_input("Formato: 4-10:2.54, 3-7:2.75", "")

# --- MOTORE (LOGICA V1) ---
if st.button("🚀 CALCOLA"):
    try:
        # Parser Cavalli
        lines = [l.strip() for l in input_cavalli.split('\n') if l.strip()]
        data_cavalli = {'numero': [], 'quota_vincente': []}
        curr_n = None
        for line in lines:
            if line.isdigit(): curr_n = int(line)
            elif "Vincente" in line and curr_n:
                data_cavalli['numero'].append(curr_n)
                data_cavalli['quota_vincente'].append(float(line.replace("Vincente", "").strip()))
                curr_n = None
        
        df = pd.DataFrame(data_cavalli)
        df['prob_mercato'] = (1/df['quota_vincente']) / (1/df['quota_vincente']).sum()
        
        # Simulazione Monte Carlo
        n_sim = 100000
        conteggi = {c.split(':')[0]: 0 for c in input_coppie.split(",") if ":" in c}
        rng = np.random.default_rng()
        
        for _ in range(n_sim):
            podio = rng.choice(df['numero'], size=3, replace=False, p=df['prob_mercato'])
            for c_str in conteggi:
                c1, c2 = map(int, c_str.split("-"))
                if c1 in podio and c2 in podio: conteggi[c_str] += 1
        
        # Risultati
        st.subheader("💰 Verdetto")
        for c_str, vinte in conteggi.items():
            prob = vinte / n_sim
            quota = float(input_coppie.split(c_str+":")[1].split(",")[0])
            roi = (prob * quota) - 1
            if roi > 0:
                puntata = min(np.floor((roi/(quota-1)) * budget * frazione_kelly), max_puntata)
                if puntata >= 2: st.success(f"**{c_str}**: {int(puntata)}€ (ROI {roi:.1%})")
                
    except Exception as e: st.error(f"Errore: {e}")