import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==============================
# Pfad zu den CSV-Dateien
# C:\Users\joris\Documents\IPJ1\Daten\Verbrauch.csv
# C:\Users\joris\Documents\IPJ1\Daten\Erzeugung.csv
# ==============================   

pfaderzeugung = "C:\\Users\\joris\\Documents\\IPJ1\\Daten\\Erzeugung.csv"
pfadverbrauch = "C:\\Users\\joris\\Documents\\IPJ1\\Daten\\Verbrauch.csv"

# ==============================
# 1. CSV-Dateien einlesen
# ==============================

erzeugung = pd.read_csv(pfaderzeugung, sep=";", low_memory=False)
verbrauch = pd.read_csv(pfadverbrauch, sep=";", low_memory=False)

# ==============================
# 2. Datumsangaben konvertieren
# ==============================

erzeugung["Datum von"] = pd.to_datetime(erzeugung["Datum von"], format="%d.%m.%Y %H:%M")
verbrauch["Datum von"] = pd.to_datetime(verbrauch["Datum von"], format="%d.%m.%Y %H:%M")

# ==============================
# 3. Anpassen der Datein (Entfernen von Leerzeichen in Spaltennamen etc.)
# ==============================

for col in erzeugung.columns:
    if "MWh" in col:
        erzeugung[col] = (
            erzeugung[col]
            .astype(str)
            .str.replace("-", "0", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

for col in verbrauch.columns:
    if "MWh" in col:
        verbrauch[col] = (
            verbrauch[col]
            .astype(str)
            .str.replace("-", "0", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

# ==============================
# 4. Erneuerbare Energien zusammenfassen
# ==============================

erneuerbare_cols = [
    "Biomasse [MWh] Originalauflösungen",
    "Wasserkraft [MWh] Originalauflösungen",
    "Wind Offshore [MWh] Originalauflösungen",
    "Wind Onshore [MWh] Originalauflösungen",
    "Photovoltaik [MWh] Originalauflösungen",
    "Sonstige Erneuerbare [MWh] Originalauflösungen",
]

erzeugung["Erneuerbare [MWh]"] = erzeugung[erneuerbare_cols].sum(axis=1)

# ==============================
# 5. verbrauch und erzeugung zusammenführen und anteile berechnen
# ==============================

gesamt = pd.merge(
    erzeugung[["Datum von", "Erneuerbare [MWh]"]],
    verbrauch[["Datum von", "Netzlast [MWh] Originalauflösungen"]],
    on="Datum von",
    how="inner",
)

gesamt["Anteil Erneuerbare [MWh]"] = (
    gesamt["Erneuerbare [MWh]"] / gesamt["Netzlast [MWh] Originalauflösungen"] * 100
).round(2)

# ==============================
# 6. Ergebnisse in eine Excel-Datei speichern
# ==============================
gesamt.to_excel(
    "C:\\Users\\joris\\Documents\\IPJ1\\Daten\\Analyse_Erneuerbare_Anteil.xlsx",
    index=False,
)
