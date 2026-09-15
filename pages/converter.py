import streamlit as st

st.title("✂️ Convertitore SNAI")
st.write("Incolla qui sotto il testo grezzo copiato dal sito SNAI:")

raw_text = st.text_area("Testo copiato dal sito", height=200)

if st.button("Converti in stringa"):
    lines = raw_text.split('\n')
    data = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if '-' in line and ' ' not in line: # Identifica la coppia (es: "10-11")
            coppia = line
            # La riga successiva contiene le quote "X.XX - Y.YY"
            if i + 1 < len(lines):
                quote_line = lines[i+1].strip()
                try:
                    quota_min = float(quote_line.split('-')[0].strip())
                    data.append((coppia, quota_min))
                except:
                    pass
            i += 2
        else:
            i += 1
    
    # Ordiniamo per quota minima
    data.sort(key=lambda x: x[1])
    
    # Creiamo la stringa finale
    final_string = ", ".join([f"{c}:{q}" for c, q in data])
    
    st.success("Stringa pronta da copiare:")
    st.code(final_string)
