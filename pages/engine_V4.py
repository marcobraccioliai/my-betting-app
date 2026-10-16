import streamlit as st
import numpy as np
import pandas as pd
from math import sqrt

# Stile: Azzurro tenue
st.markdown("""<style>.stApp {background-color: #E1F5FE;}</style>""", unsafe_allow_html=True)

st.title("⚙️ Engine V4 (Motore di Simulazione)")

# --- CONFIGURAZIONE (Expander come da template) ---
with st.expander("⚙️ Impostazioni Budget", expanded=False):
    budget = st.number_input("Budget Totale (€)", value=200.0)
    max_puntata = st.number_input("Limite Singola Puntata (€)", value=10.0)
    kelly_frac = st.slider("Prudenza (Frazione Kelly)", 0.1, 1.0, 0.5)

# --- INPUT DATI ---
st.subheader("📥 Input Dati")
cavalli_raw = st.text_area("Incolla stringa Parser (Cavalli):", height=100)
accoppiata_raw = st.text_area("Incolla stringa Converter (Accoppiate):", height=100)

if st.button("🚀 CALCOLA ANALISI"):
    try:
        # 1. Parsing Cavalli
        temp_dati = {"numero":[], "quota_vincente":[], "piazzato_min":[], "piazzato_max":[]}
        for cavallo in cavalli_raw.strip().split(';'):
            num, vals = cavallo.split(':')
            v, pmin, pmax = map(float, vals.split(','))
            temp_dati["numero"].append(int(num))
            temp_dati["quota_vincente"].append(v)
            temp_dati["piazzato_min"].append(pmin)
            temp_dati["piazzato_max"].append(pmax)
        df = pd.DataFrame(temp_dati)
        
        # 2. Parsing Accoppiate
        quote_dict = {}
        for item in accoppiata_raw.split(','):
            coppia_str, quota_str = item.split(':')
            c1, c2 = coppia_str.strip().split('-')
            quote_dict[(int(c1), int(c2))] = float(quota_str.strip())
            
        # 3. Motore V4 (Logica Pietra Miliare)
        df["p_v"] = (1/df["quota_vincente"]) / (1/df["quota_vincente"]).sum()
        df["p_p"] = (1/((df["piazzato_min"]+df["piazzato_max"])/2)) / (1/((df["piazzato_min"]+df["piazzato_max"])/2)).sum()
        df["forza"] = (df["p_v"]**0.5) * (df["p_p"]**0.5)
        df["forza"] /= df["forza"].sum()
        
        rng = np.random.default_rng(None)
        conteggi = {c: 0 for c in quote_dict.keys()}
        
        for _ in range(200000):
            podio = set(rng.choice(df["numero"].to_numpy(), size=3, replace=False, p=df["forza"].to_numpy()))
            for c in conteggi:
                if c[0] in podio and c[1] in podio: conteggi[c] += 1
        
        risultati = []
        for c, v in conteggi.items():
            p = v / 200000
            q = quote_dict[c]
            risultati.append({"Coppia": f"{c[0]}-{c[1]}", "Prob": p, "Quota": q, "Edge": p - (1/q), "ROI": (p * q) - 1})
            
        df_res = pd.DataFrame(risultati)
        
        # 4. Selezione Scommesse
        df_scelte = df_res[(df_res["Prob"] >= 0.35) & (df_res["Edge"] >= 0.05) & (df_res["ROI"] >= 0.10)].copy()
        df_scelte["Puntata"] = (np.floor((df_scelte["ROI"]/(df_scelte["Quota"]-1) * budget * kelly_frac).clip(0, max_puntata) / 1.0) * 1.0)
        df_scelte = df_scelte[df_scelte["Puntata"] >= 2.0].sort_values("Prob", ascending=False)
        
        # Output
        st.subheader("💰 Verdetto")
        st.dataframe(df_res[["Coppia", "Quota", "Prob", "Edge", "ROI"]].style.format({'Prob':'{:.2%}', 'Edge':'{:.2%}', 'ROI':'{:.2%}'}))
        
        if df_scelte.empty:
            st.warning("Nessuna scommessa trovata.")
        else:
            for _, row in df_scelte.iterrows():
                st.success(f"PUNTA {row['Puntata']}€ SU {row['Coppia']} (Q:{row['Quota']})")
                
    except Exception as e:
        st.error(f"Errore: {e}. Controlla il formato dell'input.")
