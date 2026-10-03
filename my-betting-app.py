import streamlit as st
import numpy as np
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="SocioBet Cesena", layout="centered")

st.title("🏇 SocioBet: Strategia Ippica")
st.write("Inserisci i dati del monitor e calcola il valore.")

# --- SEZIONE 1: CONFIGURAZIONE CORSA ---
with st.expander("⚙️ Impostazioni Budget", expanded=False):
    budget = st.number_input("Budget Totale (€)", value=200)
    max_puntata = st.number_input("Limite Singola Puntata (€)", value=10)
    frazione_kelly = st.slider("Prudenza (Frazione Kelly)", 0.1, 1.0, 0.5)

# --- NUOVA SEZIONE 2: DINAMICA ---
st.subheader("📊 Dati Vincenti & Sferratura")
num_cavalli = st.number_input("Quanti cavalli corrono?", min_value=1, max_value=24, value=12)

cavalli_data = []
for i in range(1, num_cavalli + 1):
    # Valori di default per questa specifica corsa (Corsa 5 Cesena)
    # Puoi lasciarli a 10.0 e cambiarli a mano nell'app
    cavalli_data.append({
        "N": i,
        "Ritirato": False,
        "Quota Fissa": 10.0,
        "Sferrato (SS)": False
    })

df_input = st.data_editor(
    pd.DataFrame(cavalli_data),
    column_config={
        "N": st.column_config.NumberColumn(disabled=True),
        "Quota Fissa": st.column_config.NumberColumn(format="%.2f"),
    },
    hide_index=True,
    use_container_width=True
)

# --- SEZIONE 3: ACCOPPIATE PIAZZATE ---
st.subheader("🎯 Accoppiate Piazzate (Monitor)")
st.write("Inserisci le coppie che stai monitorando e la quota minima")
# Esempio di input rapido: "4-10:2.54, 3-7:2.75"
input_coppie = st.text_input("Formato: 4-10:2.54, 3-7:2.75", "")

# --- SEZIONE 4: CALCOLO ---
if st.button("🚀 CALCOLA PUNTATE OTTIMALI", use_container_width=True):
    # Filtriamo i ritirati
    df_active = df_input[df_input["Ritirato"] == False].copy()
    
    # Calcolo probabilità base
    df_active['prob'] = 1 / df_active['Quota Fissa']
    
    # Applichiamo un piccolo bonus (5%) se sferrato (SS)
    df_active.loc[df_active['Sferrato (SS)'] == True, 'prob'] *= 1.05
    
    # Normalizzazione
    df_active['prob_norm'] = df_active['prob'] / df_active['prob'].sum()
    
    # Simulazione Monte Carlo
    n_sim = 100000 
    conteggio = {}
    
    # Parsing coppie
    try:
        coppie_list = [c.strip() for c in input_coppie.split(",")]
        for item in coppie_list:
            coppia_str, quota = item.split(":")
            c1, c2 = map(int, coppia_str.split("-"))
            conteggio[(c1, c2)] = [0, float(quota)]
            
        # Simulazione
        numeri = df_active['N'].values
        probs = df_active['prob_norm'].values
        
        for _ in range(n_sim):
            podio = np.random.choice(numeri, size=3, replace=False, p=probs)
            for coppia in conteggio:
                if coppia[0] in podio and coppia[1] in podio:
                    conteggio[coppia][0] += 1
        
        # --- RACCOLTA E ORDINAMENTO RISULTATI ---
        valid_results = []
        low_stake_results = []
        
        for coppia, dati in conteggio.items():
            p_sim = dati[0] / n_sim
            quota_mkt = dati[1]
            roi = (p_sim * quota_mkt) - 1
            
            if roi > 0:
                f_k = roi / (quota_mkt - 1)
                puntata = min(np.floor(f_k * budget * frazione_kelly), max_puntata)
                
                result_item = {
                    'coppia': coppia,
                    'roi': roi,
                    'puntata': int(puntata)
                }
                
                if puntata >= 2:
                    valid_results.append(result_item)
                else:
                    low_stake_results.append(result_item)
                    
        # Ordinamento per ROI decrescente (dal più alto al più basso)
        valid_results = sorted(valid_results, key=lambda x: x['roi'], reverse=True)
        low_stake_results = sorted(low_stake_results, key=lambda x: x['roi'], reverse=True)
        
        # Risultati a schermo
        st.divider()
        st.subheader("💰 Verdetto dello Sportello")
        
        if valid_results or low_stake_results:
            # Mostra prima le scommesse valide ordinate per ROI
            for res in valid_results:
                c1, c2 = res['coppia']
                st.success(f"**COPPIA {c1}-{c2}**")
                st.write(f"👉 PUNTA: **{res['puntata']} €**")
                st.write(f"📈 ROI Stimato: {res['roi']:.1%}")
                
            # Mostra quelle con puntata sotto i 2€
            for res in low_stake_results:
                c1, c2 = res['coppia']
                st.warning(f"Coppia {c1}-{c2}: Valore positivo (ROI: {res['roi']:.1%}) ma puntata sotto il minimo di 2€.")
        else:
            st.error("Nessun valore trovato. Meglio non scommettere su queste coppie.")
            
    except Exception as e:
        st.error(f"Errore nell'inserimento dati: {e}")
