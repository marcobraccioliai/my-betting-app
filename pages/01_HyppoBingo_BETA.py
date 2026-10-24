import streamlit as st
import numpy as np
import pandas as pd

# Stile grafico: Rosso Porpora per identificazione immediata
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

with st.expander("⚙️ Impostazioni Budget", expanded=False):
    budget = st.number_input("Budget Totale (€)", value=200)
    max_puntata = st.number_input("Limite Singola Puntata (€)", value=10)
    frazione_kelly = st.slider("Prudenza (Frazione Kelly)", 0.1, 1.0, 0.5)

# --- INPUT A PASTONE ---
st.subheader("1. Incolla Dati Cavalli")
input_cavalli = st.text_area("Formato: 4 (riga) Vincente 2.80", height=150)

st.subheader("2. Incolla Accoppiate")
st.write("Inserisci le coppie che stai monitorando e la quota minima (prese da Converter Quote ACP NX)")
input_coppie = st.text_input("Formato: 4-10:2.54, 3-7:2.75", "")

# --- MOTORE (LOGICA V1) ---
if st.button("🚀🚀🚀🚀"):
    try:
        # Parsing Cavalli (Nuovo formato N:Quota)
        lines = [i.strip() for i in input_cavalli.replace('\n', ',').split(',') if i.strip()]
        data_cavalli = {'numero': [], 'quota_vincente': []}
        for item in lines:
            if ':' in item:
                n, q = item.split(':')
                data_cavalli['numero'].append(int(n))
                data_cavalli['quota_vincente'].append(float(q))
        
        df = pd.DataFrame(data_cavalli)
        # Assicuriamo che il dataframe non sia vuoto
        if df.empty:
            st.error("Nessun cavallo trovato. Controlla il formato stringa.")
            st.stop()
            
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
