import streamlit as st
import pandas as pd

st.set_page_config(page_title="Parser Cavalli", layout="centered")

st.title("✂️ Parser Cavalli SNAI")

# Input
raw_text = st.text_area("Incolla qui il testo grezzo copiato da SNAI:", height=300)

if st.button("Converti Dati"):
    try:
        lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
        data = []
        current_horse = None
        
        for i, line in enumerate(lines):
            # Cerca il numero del cavallo (righe contenenti solo cifre, escludendo rank tipo 1°)
            # Esempio: se la riga è "4", viene presa. Se è "1°", viene saltata.
            if line.isdigit():
                current_horse = int(line)
            
            # Cerca la quota vincente
            if "Vincente" in line and current_horse:
                try:
                    quota = float(line.replace("Vincente", "").strip())
                    data.append({"N": current_horse, "Quota Fissa": quota, "Ritirato": False, "Sferrato (SS)": False})
                    current_horse = None # Reset dopo aver trovato la quota
                except:
                    pass
        
        if data:
            df = pd.DataFrame(data)
            st.success("Dati estratti con successo:")
            st.dataframe(df, use_container_width=True)
            st.write("Puoi copiare questi dati o usarli per aggiornare la griglia.")
        else:
            st.warning("Nessun dato trovato. Assicurati che il formato contenga 'Vincente X.XX'")
            
    except Exception as e:
        st.error(f"Errore durante il parsing: {e}")