import re

import streamlit as st


st.set_page_config(page_title="Parser Cavalli", layout="centered")

st.markdown(
    """
    <style>
    /* 1. Sfondo rosso porpora solo per l'area principale */
    [data-testid="stAppViewContainer"] {
        background-color: #B20000 !important;
    }

    /* 2. Testo crema solo per l'area principale */
    .stApp div[data-testid="stMarkdownContainer"],
    .stApp label,
    .stApp h1, .stApp h2, .stApp h3 {
        color: #FFFDD0 !important;
    }

    /* 3. Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F0F2F6 !important;
    }

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
    """,
    unsafe_allow_html=True,
)

st.title("✂️ Converter Quote Singoli Cavalli")
st.write(
    "Incolla qui sotto il testo grezzo copiato dal sito SNAI "
    "(quote fisse del cavallo vincente)."
)

raw_text = st.text_area("Incolla testo grezzo:", height=200)


def extract_fixed_odds(text):
    """
    Estrae la quota FISSA di ciascun cavallo da un pastone SNAI.

    Formati riconosciuti:
      - Desktop:    Vincente 9.00
      - Smartphone: V 9.00

    Le quote al totalizzatore (ad esempio VIN seguito da una quota)
    vengono ignorate.

    Se lo stesso cavallo compare più volte nel testo, viene mantenuta
    soltanto la prima quota fissa incontrata.
    """

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # I dizionari Python mantengono l'ordine di inserimento e impediscono
    # che una tabella duplicata produca cavalli duplicati.
    results = {}
    current_horse = None

    # Accetta soltanto le diciture della quota fissa:
    # "Vincente 9.00" (desktop) oppure "V 9.00" (smartphone).
    # "VIN" non corrisponde a questa espressione e viene ignorato.
    fixed_odds_pattern = re.compile(
        r"^(?:Vincente|V)\s+([0-9]+(?:[.,][0-9]+)?)$",
        re.IGNORECASE,
    )

    for line in lines:

        # Un numero isolato identifica il numero del cavallo.
        if line.isdigit():
            current_horse = line
            continue

        match = fixed_odds_pattern.fullmatch(line)

        if match and current_horse is not None:

            # Se il cavallo è già stato acquisito, mantiene la prima quota.
            if current_horse not in results:
                quota = float(match.group(1).replace(",", "."))

                # Mantiene il comportamento del programma originale.
                if quota <= 1.0:
                    quota = 1000.0

                results[current_horse] = f"{current_horse}:{quota:.2f}"

            current_horse = None

    return ", ".join(results.values())


if st.button("🚀🚀🚀🚀"):
    try:
        output = extract_fixed_odds(raw_text)

        if output:
            st.code(output)
        else:
            st.error(
                "Nessun dato estratto. Verifica di aver incollato "
                "il testo delle quote SNAI."
            )

    except Exception as error:
        st.error(f"Errore durante l'elaborazione: {error}")
