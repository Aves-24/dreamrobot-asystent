import streamlit as st
import re

st.set_page_config(page_title="Asystent Wysyłek Dreamrobot", layout="wide")

# --- BAZA WIEDZY ---
# W prawdziwej aplikacji te dane będą zapisywać się w pliku, żeby nie znikały.
# Na razie wpisałem na sztywno Twoje reguły dla toreb Seniori.
if 'baza_produktow' not in st.session_state:
    st.session_state.baza_produktow = {
        "flex": {1: "DHL Kleinpaket", 2: "bis 1kg", 3: "bis 2kg", 4: "bis 3kg"},
        "v-model": {1: "DHL Kleinpaket", 2: "bis 1kg", 3: "bis 2kg", 4: "bis 3kg"},
        # Jeśli w nazwie jest "seniori", ale nie ma "flex" ani "v-model", to traktujemy jako Classic:
        "seniori": {1: "bis 1kg", 2: "bis 1kg", 3: "bis 1kg", 4: "bis 3kg"} 
    }

opcje_dhl = ["DHL Kleinpaket", "bis 1kg", "bis 2kg", "bis 3kg", "bis 5kg", "bis 10kg", "bis 30kg"]

# --- ZAKŁADKI W APLIKACJI WEBOWEJ ---
zakladka_pracownik, zakladka_manager = st.tabs(["📦 Panel Pracownika", "⚙️ Kreator Reguł (Manager)"])

# ==========================================
# ZAKŁADKA 1: PANEL PRACOWNIKA
# ==========================================
with zakladka_pracownik:
    st.header("Co mam zaznaczyć?")
    wklejony_tekst = st.text_input("Wklej całą nazwę skopiowaną z Dreamrobot:")

    if wklejony_tekst:
        # Szukamy ilości na początku (np. "3 x", "2x")
        match_ilosc = re.search(r'^(\d+)\s*[xX]', wklejony_tekst)
        ilosc = int(match_ilosc.group(1)) if match_ilosc else 1
        
        # Ograniczamy do max 4, jak prosiłeś (jeśli więcej, traktujemy jako 4 lub można dodać alert)
        if ilosc > 4:
            st.warning("Uwaga! Ilość większa niż 4. Wynik może być niedokładny.")
            ilosc = 4

        tekst_lower = wklejony_tekst.lower()
        znaleziony_wynik = None
        rozpoznany_produkt = "Nieznany"

        # Logika szukania słów kluczowych
        # Najpierw szukamy specyficznych modeli (flex, v-model)
        if "flex" in tekst_lower:
            znaleziony_wynik = st.session_state.baza_produktow["flex"][ilosc]
            rozpoznany_produkt = "Seniori Flex"
        elif "v-model" in tekst_lower:
            znaleziony_wynik = st.session_state.baza_produktow["v-model"][ilosc]
            rozpoznany_produkt = "Seniori V-Model"
        elif "seniori" in tekst_lower:
            znaleziony_wynik = st.session_state.baza_produktow["seniori"][ilosc]
            rozpoznany_produkt = "Seniori Classic / Universal"

        # Wyświetlanie wyniku pracownikowi
        if znaleziony_wynik:
            st.success(f"Rozpoznano produkt: **{rozpoznany_produkt}** | Ilość: **{ilosc} szt.**")
            st.metric(label="Zaznacz w systemie:", value=znaleziony_wynik)
        else:
            st.error("Nie znalazłem reguły dla tego produktu. Zapytaj przełożonego!")

# ==========================================
# ZAKŁADKA 2: KREATOR REGUŁ
# ==========================================
with zakladka_manager:
    st.header("Szybkie dodawanie nowych produktów")
    st.markdown("Dodaj nowy produkt i zdefiniuj, co pracownik ma kliknąć w zależności od ilości w koszyku.")
    
    nowa_nazwa = st.text_input("Słowo kluczowe w nazwie (np. 'parasol', 'wiatrołap'):").lower()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        wybor_1 = st.selectbox("Dla 1 sztuki:", opcje_dhl, key="w1")
    with col2:
        wybor_2 = st.selectbox("Dla 2 sztuk:", opcje_dhl, key="w2")
    with col3:
        wybor_3 = st.selectbox("Dla 3 sztuk:", opcje_dhl, key="w3")
    with col4:
        wybor_4 = st.selectbox("Dla 4 sztuk:", opcje_dhl, key="w4")

    if st.button("Zapisz regułę"):
        if nowa_nazwa:
            st.session_state.baza_produktow[nowa_nazwa] = {
                1: wybor_1, 2: wybor_2, 3: wybor_3, 4: wybor_4
            }
            st.success(f"Dodano regułę dla '{nowa_nazwa}'!")
