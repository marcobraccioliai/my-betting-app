import re
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Ottimizzatore Scommesse", page_icon="🎯", layout="centered"
)

st.title("🎯 Ottimizzatore e Normalizzatore Scommesse")
st.markdown(
    "Incolla qui sotto il testo grezzo (RAW) del simulatore (anche su più"
    " righe). L'app pulirà i dati, normalizzerà le puntate (target ~10€, range"
    " 8-12€) e gestirà in autonomia i vincoli minimi e di budget."
)

# Area di input per il testo RAW
raw_input = st.text_area(
    "Testo RAW delle scommesse:",
    height=200,
    placeholder=(
        "Incolla qui le stringhe...\nEs:\n** 1-5**: 3€ (ROI 10.9%)\n** 1-2**:"
        " 2€ (ROI 38.4%)"
    ),
)

if st.button("Elabora e Ottimizza", type="primary"):
  if not raw_input.strip():
    st.warning("Per favore, inserisci del testo valido.")
  else:
    logs = []

    # 1. PARSING: Estrae coppia, puntata e ROI (gestisce asterischi e righe multiple)
    pattern = r"\*{0,2}\s*([0-9A-Za-z\-]+)\*{0,2}\s*:\s*([0-9\.,]+)€?\s*\(\s*ROI\s*([0-9\.,]+)%\s*\)"
    matches = re.findall(pattern, raw_input)

    if not matches:
      st.error(
          "Nessun formato valido trovato. Controlla che il testo contenga le"
          " coppie, le quote e i ROI nel formato corretto."
      )
    else:
      bets = []
      for match in matches:
        pair, stake, roi = match
        bets.append({
            "pair": pair.strip(),
            "stake": float(stake.replace(",", ".")),
            "roi": float(roi.replace(",", ".")),
        })

      logs.append(f"Trovate {len(bets)} scommesse nel testo in ingresso.")

      # 2. CALCOLO TARGET E SCALING
      orig_total = sum(b["stake"] for b in bets)
      logs.append(f"Spesa totale originale: {orig_total}€")

      target_total = 10.0
      scale_factor = (target_total / orig_total) if orig_total > 0 else 1.0

      # Assegnazione provvisoria scalata e arrotondata a intero
      for b in bets:
        raw_scaled = b["stake"] * scale_factor
        b["current_stake"] = max(1, round(raw_scaled))

      logs.append("Applicata normalizzazione proporzionale iniziale.")

      # 3. APPLICAZIONE REGOLE: SOGLIA MINIMA (2€) E FALLBACK ROI
      changed = True
      while changed:
        changed = False
        current_total = sum(b["current_stake"] for b in bets)

        # Cerca puntate sotto i 2€
        below_min = [b for b in bets if b["current_stake"] < 2]

        if below_min:
          b_low = below_min[0]
          old_stake = b_low["current_stake"]
          b_low["current_stake"] = 2  # Forziamo al minimo di 2€

          new_total = sum(b["current_stake"] for b in bets)
          if new_total <= 12:
            logs.append(
                f"Coppia {b_low['pair']}: puntata troppo bassa ({old_stake}€)."
                " Forzata al minimo di 2€."
            )
            changed = True
          else:
            # Se forzarla fa superare i 12€, rimuoviamo la peggiore per ROI
            b_low["current_stake"] = old_stake  # Ripristiniamo
            bets.sort(key=lambda x: x["roi"])
            removed = bets.pop(0)
            logs.append(
                "Vincolo superato (Totale > 12€). Rimossa la coppia"
                f" {removed['pair']} (ROI {removed['roi']}%) per far"
                " rientrare il budget."
            )
            changed = True

        elif current_total > 12:
          # Se il totale sfora comunque i 12€, eliminiamo la peggiore per ROI
          bets.sort(key=lambda x: x["roi"])
          removed = bets.pop(0)
          logs.append(
              f"Totale ({current_total}€) sopra il limite di 12€. Rimossa la"
              f" coppia con ROI più basso: {removed['pair']} (ROI"
              f" {removed['roi']}%)."
          )
          changed = True

      # Riordiniamo le scommesse per comodità visiva (opzionale, es. per coppia o ROI)
      # bets.sort(key=lambda x: x['pair'])

      # 4. COSTRUZIONE OUTPUT FINALE
      st.success("Elaborazione completata con successo!")

      final_string_parts = []
      for b in bets:
        final_string_parts.append(
            f"{b['pair']}: {b['current_stake']}€ (ROI {b['roi']}%)"
        )

      final_string = "\n".join(final_string_parts)

      st.subheader("📋 Stringa Ottimizzata (Pronta da copiare)")
      st.code(final_string, language="text")

      final_total = sum(b["current_stake"] for b in bets)
      st.metric(
          label="Spesa Totale Finale",
          value=f"{final_total}€",
          delta=f"Target: {target_total}€ (Range: 8-12€)",
      )

      with st.expander(
          "🔍 Log Dettagliato delle Decisioni (Trasparenza Algoritmo)"
      ):
        for log in logs:
          st.write(f"- {log}")
