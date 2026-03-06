import streamlit as st
import re

st.set_page_config(page_title="Versandassistent Dreamrobot", layout="wide")

# --- WISSENSBATT / BAZA WIEDZY ---
if 'baza_produktow' not in st.session_state:
    st.session_state.baza_produktow = {
        "flex": {1: "DHL Kleinpaket", 2: "bis 1kg", 3: "bis 2kg", 4: "bis 3kg"},
        "v-model": {1: "DHL Kleinpaket", 2: "bis 1kg", 3: "bis 2kg", 4: "bis 3kg"},
        "seniori": {1: "bis 1kg", 2: "bis 1kg", 3: "bis 1kg", 4: "bis 3kg"} 
    }

opcje_dhl = ["DHL Kleinpaket", "bis 1kg", "bis 2kg", "bis 3kg", "bis 5kg", "bis 10kg", "bis 30kg"]

# --- TABS / ZAKŁADKI ---
zakladka_pracownik, zakladka_manager = st.tabs(["📦 Mitarbeiter-Panel", "⚙️ Regel-Manager"])

# ==========================================
# ZAKŁADKA 1: PANEL PRACOWNIKA (MITARBEITER)
# ==========================================
with zakladka_pracownik:
    st.header("Was soll ich auswählen?")
    wklejony_tekst = st.text_input("Füge den kompletten Artikelnamen aus Dreamrobot hier ein:")

    if wklejony_tekst:
        match_ilosc = re.search(r'^(\d+)\s*[xX]', wklejony_tekst)
        ilosc = int(match_ilosc.group(1)) if match_ilosc else 1
        
        if ilosc > 4:
            st.warning("Achtung! Menge größer als 4. Das Ergebnis könnte ungenau sein.")
            ilosc = 4

        tekst_lower = wklejony_tekst.lower()
        znaleziony_wynik = None
        rozpoznany_produkt = "Unbekannt"

        if "flex" in tekst_lower:
            znaleziony_wynik = st.session_state.baza_produktow["flex"][ilosc]
            rozpoznany_produkt = "Seniori Flex"
        elif "v-model" in tekst_lower:
            znaleziony_wynik = st.session_state.baza_produktow["v-model"][ilosc]
            rozpoznany_produkt = "Seniori V-Model"
        elif "seniori" in tekst_lower:
            znaleziony_wynik = st.session_state.baza_produktow["seniori"][ilosc]
            rozpoznany_produkt = "Seniori Classic / Universal"

        if znaleziony_wynik:
            st.success(f"Erkanntes Produkt: **{rozpoznany_produkt}** | Menge: **{ilosc} Stk.**")
            st.metric(label="Im System auswählen:", value=znaleziony_wynik)
        else:
            st.error("Keine Regel für dieses Produkt gefunden. Bitte den Vorgesetzten fragen!")

# ==========================================
# ZAKŁADKA 2: KREATOR REGUŁ (MANAGER)
# ==========================================
with zakladka_manager:
    st.header("Schnelles Hinzufügen neuer Produkte")
    st.markdown("Füge ein neues Produkt hinzu und definiere, was der Mitarbeiter je nach Menge im Warenkorb anklicken soll.")
    
    nowa_nazwa = st.text_input("Schlüsselwort im Namen (z.B. 'Windschutz', 'Tasche'):").lower()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        wybor_1 = st.selectbox("Für 1 Stück:", opcje_dhl, key="w1")
    with col2:
        wybor_2 = st.selectbox("Für 2 Stück:", opcje_dhl, key="w2")
    with col3:
        wybor_3 = st.selectbox("Für 3 Stück:", opcje_dhl, key="w3")
    with col4:
        wybor_4 = st.selectbox("Für 4 Stück:", opcje_dhl, key="w4")

    if st.button("Regel speichern"):
        if nowa_nazwa:
            st.session_state.baza_produktow[nowa_nazwa] = {
                1: wybor_1, 2: wybor_2, 3: wybor_3, 4: wybor_4
            }
            st.success(f"Regel für '{nowa_nazwa}' hinzugefügt!")
