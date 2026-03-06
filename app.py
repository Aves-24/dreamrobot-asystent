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

opcje_dhl = ["DHL Kleinpaket", "bis 1kg", "bis 2kg", "bis 3kg", "bis 5kg", "bis 10kg", "bis 16kg", "bis 20kg", "bis 30kg", "bis 31,5kg"]

# --- TABS / ZAKŁADKI ---
zakladka_pracownik, zakladka_manager = st.tabs(["📦 Mitarbeiter-Panel", "⚙️ Regel-Manager"])

# ==========================================
# ZAKŁADKA 1: PANEL PRACOWNIKA (MITARBEITER)
# ==========================================
with zakladka_pracownik:
    st.header("Was soll ich auswählen?")
    
    # Przełącznik trybu pracy
    tryb = st.radio("Wähle den Eingabemodus:", 
                    ["📝 Text aus Dreamrobot einfügen", "🔍 Manuelle Produktsuche (Autovervollständigung)"], 
                    horizontal=True)
    
    st.divider()

    if tryb == "📝 Text aus Dreamrobot einfügen":
        wklejony_tekst = st.text_input("Füge den kompletten Artikelnamen aus Dreamrobot hier ein:")

        if wklejony_tekst:
            match_ilosc = re.search(r'^(\d+)\s*[xX]', wklejony_tekst)
            ilosc = int(match_ilosc.group(1)) if match_ilosc else 1
            
            if ilosc > 4:
                st.warning("Achtung! Menge größer als 4. Das Ergebnis wird für 4 Stück berechnet.")
                ilosc = 4

            tekst_lower = wklejony_tekst.lower()
            znaleziony_wynik = None
            rozpoznany_produkt = "Unbekannt"

            for klucz in st.session_state.baza_produktow.keys():
                if klucz in tekst_lower:
                    znaleziony_wynik = st.session_state.baza_produktow[klucz][ilosc]
                    rozpoznany_produkt = klucz.title()
                    break 

            if znaleziony_wynik:
                st.success(f"Erkanntes Produkt: **{rozpoznany_produkt}** | Menge: **{ilosc} Stk.**")
                st.metric(label="Im System auswählen:", value=znaleziony_wynik)
            else:
                st.error("Keine Regel für dieses Produkt gefunden. Bitte den Vorgesetzten fragen!")

    else: # Tryb Autocomplete
        lista_opcji = ["-- Bitte tippen oder wählen --"] + list(st.session_state.baza_produktow.keys())
        
        col_auto1, col_auto2 = st.columns([3, 1])
        with col_auto1:
            wybrany_klucz = st.selectbox("Tippe, um das Produkt zu suchen:", lista_opcji)
        with col_auto2:
            ilosc_reczna = st.number_input("Menge:", min_value=1, max_value=4, value=1)
            
        if wybrany_klucz != "-- Bitte tippen oder wählen --":
            znaleziony_wynik = st.session_state.baza_produktow[wybrany_klucz][ilosc_reczna]
            st.success(f"Ausgewähltes Produkt: **{wybrany_klucz.title()}** | Menge: **{ilosc_reczna} Stk.**")
            st.metric(label="Im System auswählen:", value=znaleziony_wynik)

# ==========================================
# ZAKŁADKA 2: KREATOR REGUŁ (MANAGER)
# ==========================================
with zakladka_manager:
    st.header("Regeln verwalten")
    
    st.subheader("Aktuelle Regeln bearbeiten")
    
    if not st.session_state.baza_produktow:
        st.info("Die Liste ist leer. Füge unten neue Produkte hinzu.")
    else:
        lista_produktow = ["-- Wähle ein Produkt --"] + list(st.session_state.baza_produktow.keys())
        edytowany_produkt = st.selectbox("Produkt zum Bearbeiten oder Löschen auswählen:", lista_produktow)
        
        if edytowany_produkt != "-- Wähle ein Produkt --":
            akt = st.session_state.baza_produktow[edytowany_produkt]
            idx_1 = opcje_dhl.index(akt[1]) if akt[1] in opcje_dhl else 0
            idx_2 = opcje_dhl.index(akt[2]) if akt[2] in opcje_dhl else 0
            idx_3 = opcje_dhl.index(akt[3]) if akt[3] in opcje_dhl else 0
            idx_4 = opcje_dhl.index(akt[4]) if akt[4] in opcje_dhl else 0

            st.write(f"Bearbeite Produkt: **{edytowany_produkt}**")
            col_e1, col_e2, col_e3, col_e4 = st.columns(4)
            with col_e1:
                e_wybor_1 = st.selectbox("1 Stück:", opcje_dhl, index=idx_1, key="e1")
            with col_e2:
                e_wybor_2 = st.selectbox("2 Stück:", opcje_dhl, index=idx_2, key="e2")
            with col_e3:
                e_wybor_3 = st.selectbox("3 Stück:", opcje_dhl, index=idx_3, key="e3")
            with col_e4:
                e_wybor_4 = st.selectbox("4 Stück:", opcje_dhl, index=idx_4, key="e4")

            col_zapisz, col_usun = st.columns(2)
            with col_zapisz:
                if st.button("Änderungen speichern", type="primary"):
                    st.session_state.baza_produktow[edytowany_produkt] = {1: e_wybor_1, 2: e_wybor_2, 3: e_wybor_3, 4: e_wybor_4}
                    st.success("Aktualisiert!")
                    st.rerun()
            with col_usun:
                if st.button("Produkt löschen"):
                    del st.session_state.baza_produktow[edytowany_produkt]
                    st.warning("Produkt wurde gelöscht!")
                    st.rerun()
    
    st.divider()

    st.subheader("Neues Produkt hinzufügen")
    nowa_nazwa = st.text_input("Schlüsselwort im Namen (z.B. 'windschutz'):").lower()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        wybor_1 = st.selectbox("Für 1 Stück:", opcje_dhl, key="w1")
    with col2:
        wybor_2 = st.selectbox("Für 2 Stück:", opcje_dhl, key="w2")
    with col3:
        wybor_3 = st.selectbox("Für 3 Stück:", opcje_dhl, key="w3")
    with col4:
        wybor_4 = st.selectbox("Für 4 Stück:", opcje_dhl, key="w4")

    if st.button("Neue Regel speichern"):
        if nowa_nazwa:
            if nowa_nazwa in st.session_state.baza_produktow:
                st.error("Dieses Produkt existiert bereits! Wähle es oben aus, um es zu bearbeiten.")
            else:
                st.session_state.baza_produktow[nowa_nazwa] = {
                    1: wybor_1, 2: wybor_2, 3: wybor_3, 4: wybor_4
                }
                st.success(f"Regel für '{nowa_nazwa}' hinzugefügt!")
                st.rerun()
        else:
            st.error("Bitte gib ein Schlüsselwort ein.")
