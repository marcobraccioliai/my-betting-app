import streamlit as st
import re

# Stile grafico: Giallo Paglierino per identificazione immediata
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFACD;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✂️ Parser SNAI (Data Bridge)")
st.write("Incolla qui il testo grezzo dal sito SNAI per generare la stringa di input:")

raw_text = st.text_area("Testo grezzo dal browser", height=300)

if st.button("Genera Stringa Input"):
    try:
        # Logica validata: divide in blocchi basati sul numero cavallo
        # r'\n-?\s*(\d+)\s*silks' cerca il numero cavallo che precede la parola "silks"
        blocchi = re.split(r'\n-?\s*(\d+)\s*silks', raw_text.strip())
        
        raw_input_list = []
        
        # Iterazione a blocchi (i blocchi dispari sono i numeri, i pari i contenuti)
        for i in range(1, len(blocchi), 2):
            numero = blocchi[i].strip()
            contenuto = blocchi[i+1]
            
            # Se è "Non partente", il blocco non contiene dati utili
            if "Non partente" in contenuto:
                continue
                
            # Cerchiamo tutte le quote (numeri decimali)
            quote = re.findall(r'\d+\.\d{2}', contenuto)
            
            # Prendiamo sempre e solo le prime 3 quote trovate (Ignora la 4a se presente)
            if len(quote) >= 3:
                v, pmin, pmax = quote[0], quote[1], quote[2]
                raw_input_list.append(f"{numero}:{v},{pmin},{pmax}")
        
        # Risultato finale
        final_string = "; ".join(raw_input_list)
        
        if final_string:
            st.success("Stringa generata con successo:")
            st.code(final_string)
        else:
            st.warning("Nessun dato valido trovato. Verifica il formato del testo incollato.")
            
    except Exception as e:
        st.error(f"Errore nel parsing: {e}")
