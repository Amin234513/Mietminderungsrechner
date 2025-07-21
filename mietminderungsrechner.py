import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

# ===== MAGISCHES DESIGN-SETUP =====
st.set_page_config(
    layout="wide", 
    page_title="⚖️ Mietrecht-Magie", 
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# Custom CSS für Premium-Glas-Effekt
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&family=Raleway:wght@400;800&display=swap');
:root {
    --primary: #3498db;
    --secondary: #2c3e50;
    --accent: #e74c3c;
}
body {
    background: linear-gradient(135deg, #1a2a6c, #2c3e50) fixed;
    font-family: 'Raleway', sans-serif;
    color: #ecf0f1;
}
.stApp {
    background: rgba(25, 35, 45, 0.85) !important;
    backdrop-filter: blur(10px);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin: 2rem;
    padding: 2rem;
}
.st-emotion-cache-1y4p8pa {
    padding: 3rem;
}
h1, h2, h3 {
    font-family: 'Roboto Condensed', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--primary) !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.stProgress > div > div {
    background-image: linear-gradient(90deg, #3498db, #8e44ad) !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.stSelectbox, .stNumberInput, .stDateInput {
    background: rgba(30, 40, 50, 0.7) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(52, 152, 219, 0.3) !important;
}
.stButton button {
    background: linear-gradient(90deg, var(--accent), #c0392b) !important;
    border-radius: 50px !important;
    font-weight: 800 !important;
    transition: all 0.3s ease !important;
}
.stButton button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 6px 12px rgba(231, 76, 60, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ===== INTERAKTIVE EINGABEN =====
st.title("⚖️ Mietminderungsrechner Pro")
st.subheader("Rechtssichere Berechnung mit Visualisierungen")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🔧 Grunddaten")
    miete = st.number_input("Monatliche Kaltmiete (€)", min_value=100, value=850, step=50)
    nebenkosten = st.number_input("Nebenkosten (€/Monat)", min_value=0, value=250)
    minderungsgrund = st.selectbox(
        "Minderungsgrund", 
        ["Schimmelbefall", "Heizungsausfall", "Wasserschaden", "Lärmbelästigung", "Bauarbeiten"],
        index=0
    )
    schweregrad = st.select_slider(
        "Schweregrad der Beeinträchtigung", 
        options=["Gering", "Mittel", "Erheblich", "Extrem"]
    )

with col2:
    st.markdown("### 📅 Zeitraum")
    start_date = st.date_input("Mängelbeginn", datetime.now() - timedelta(days=60))
    end_date = st.date_input("Mängelende (voraussichtlich)", datetime.now() + timedelta(days=30))
    mangel_behoben = st.toggle("Mangel bereits behoben?", False)
    
    if not mangel_behoben:
        voraussichtliche_behebung = st.date_input("Voraussichtliches Behebungsdatum", datetime.now() + timedelta(days=30))

# ===== MAGIE DER BERECHNUNG =====
# Minderungssätze basierend auf Rechtsprechung
minderungssaetze = {
    "Gering": 0.05,
    "Mittel": 0.15,
    "Erheblich": 0.30,
    "Extrem": 0.50
}

# Grunddauer berechnen
tage_mangel = (end_date - start_date).days
monate_mangel = tage_mangel / 30.42
prozentsatz = minderungssaetze[schweregrad]

# Berechnungen
minderung_pro_monat = miete * prozentsatz
gesamtminderung = monate_mangel * minderung_pro_monat

# ===== VISUALISIERUNGEN =====
st.markdown("---")
st.header("📊 Ergebnisse in Echtzeit")

# 1. Finanzielle Auswirkungen
col3, col4, col5 = st.columns(3)
col3.metric("🔻 Monatliche Mietminderung", f"{minderung_pro_monat:.2f}€")
col4.metric("⏱️ Mangelmonate", f"{monate_mangel:.1f} Monate")
col5.metric("💸 Gesamtersparnis", f"{gesamtminderung:.2f}€", delta=f"{prozentsatz*100:.0f}% Minderung")

# 2. Zeitlicher Verlauf
zeitraum = pd.date_range(start=start_date, end=end_date, freq='MS')
monatliche_werte = [miete * (1 - prozentsatz) for _ in range(len(zeitraum))]
original_miete = [miete for _ in range(len(zeitraum))]

df = pd.DataFrame({
    'Datum': zeitraum,
    'Geminderte Miete': monatliche_werte,
    'Ursprüngliche Miete': original_miete
})

fig1 = px.line(
    df, 
    x='Datum', 
    y=['Ursprüngliche Miete', 'Geminderte Miete'],
    title='<b>📈 Mietverlauf während des Mangels</b>',
    color_discrete_sequence=['#e74c3c', '#2ecc71']
)
fig1.update_layout(
    hovermode="x unified",
    yaxis_title="Miete (€)",
    xaxis_title="",
    legend_title="Mietart"
)
st.plotly_chart(fig1, use_container_width=True)

# 3. Kostenaufteilung
labels = ['Geminderte Miete', 'Minderungsbetrag']
values = [miete - minderung_pro_monat, minderung_pro_monat]

fig2 = px.pie(
    values=values, 
    names=labels, 
    hole=0.5,
    title='<b>💶 Monatliche Mietaufteilung</b>',
    color_discrete_sequence=['#3498db', '#e74c3c']
)
fig2.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig2, use_container_width=True)

# ===== RECHTLICHE HINWEISE =====
st.markdown("---")
with st.expander("ℹ️ Wichtige rechtliche Hinweise", expanded=True):
    st.warning("""
    **Dies ist keine Rechtsberatung!**  
    - Mietminderung muss schriftlich angekündigt werden  
    - Dokumentieren Sie den Mangel mit Fotos  
    - Frist zur Behebung setzen (typisch 14 Tage)  
    - Bei Streit: Mieterverein oder Anwalt konsultieren  
    """)
    
    st.info("""
    **Typische Minderungssätze laut Rechtsprechung:**  
    - Schimmelbefall: 10-30%  
    - Heizungsausfall (Winter): 50-100%  
    - Lärmbelästigung: 5-25%  
    - Wasserschaden: 10-30%  
    """)

# ===== EXPORT-OPTION =====
st.download_button(
    label="📥 PDF-Bericht generieren",
    data=f"Offizielle Mietminderung: {minderung_pro_monat:.2f}€/Monat\nGesamtersparnis: {gesamtminderung:.2f}€",
    file_name="mietminderung_berechnung.txt",
    mime="text/plain"
)

st.success("✅ Berechnung abgeschlossen! Bei weiteren Fragen konsultieren Sie bitte einen Fachanwalt für Mietrecht.")

