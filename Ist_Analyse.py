import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. CSV-Dateien einlesen
# ==============================
erzeugung = pd.read_csv("erzeugung.csv", sep=";", low_memory=False)
verbrauch = pd.read_csv("verbrauch.csv", sep=";", low_memory=False)

# ==============================
# 2. Datumsangaben konvertieren
# ==============================
erzeugung["Datum von"] = pd.to_datetime(erzeugung["Datum von"], format="%d.%m.%Y %H:%M")
verbrauch["Datum von"] = pd.to_datetime(verbrauch["Datum von"], format="%d.%m.%Y %H:%M")

# ==============================
# 3. Spalten mit MWh bereinigen Das ist eine Änderung gegenüber der ursprünglichen Version
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
# 4. Erneuerbare Energien summieren
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
# 5. Daten zusammenführen
# ==============================
df = pd.merge(
    erzeugung[["Datum von", "Erneuerbare [MWh]"]],
    verbrauch[["Datum von", "Netzlast [MWh] Originalauflösungen"]],
    on="Datum von",
    how="inner",
)

# ==============================
# 6. Anteil berechnen
# ==============================
df["Anteil Erneuerbare [%]"] = (
    df["Erneuerbare [MWh]"] / df["Netzlast [MWh] Originalauflösungen"] * 100
)

# ==============================
# Histogramm: Verteilung der EE-Anteile
# ==============================

# Definiere feste Klassen (10%, 20%, ..., 100%)
bins = np.arange(0, 110, 10)  # von 0 bis 100 in 10er-Schritten

plt.figure(figsize=(10, 6))
plt.hist(df["Anteil Erneuerbare [%]"], bins=bins, edgecolor="black")

plt.title("Verteilung des Anteils der Erneuerbaren Energien am Stromverbrauch")
plt.xlabel("Anteil Erneuerbare [%]")
plt.ylabel("Anzahl Viertelstunden")
plt.xticks(bins)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Optional: prozentuale Beschriftung über den Balken
counts, _ = np.histogram(df["Anteil Erneuerbare [%]"], bins=bins)
for i in range(len(counts)):
    plt.text(bins[i] + 5, counts[i] + counts.max() * 0.01, f"{counts[i]}", 
             ha="center", va="bottom", fontsize=8)

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(df["Anteil Erneuerbare [%]"], bins=bins, weights=np.ones(len(df)) / len(df), edgecolor="black")
plt.title("Relative Häufigkeit der EE-Anteile am Stromverbrauch")
plt.xlabel("Anteil Erneuerbare [%]")
plt.ylabel("Anteil der Viertelstunden [%]")
plt.xticks(bins)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.gca().yaxis.set_major_formatter(lambda x, _: f"{x*100:.0f}%")
plt.tight_layout()
plt.show()
