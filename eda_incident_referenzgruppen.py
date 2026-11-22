"""Erste Machbarkeitsprüfung für Kontextgruppen in BPI-2014-Incident-Logs.

Start: python eda_incident_referenzgruppen.py
Abhängigkeit: pip install pandas numpy
Verwendet die zwei CSV-Dateien in ~/Downloads.
"""
from pathlib import Path
import re
import sys
import numpy as np
import pandas as pd

BASE = Path(
    "/Users/mauricetolke/Library/Mobile Documents/com~apple~CloudDocs/Studium/Studium Master/Semester 3/Masterarbeit/Datenbasis"
)
INCIDENT = BASE / "Detail_Incident.csv"
ACTIVITY = BASE / "Detail_Incident_Activity.csv"

OUT = BASE / "Masterarbeit_EDA"
MIN_SIZES = (50, 100, 250, 500)


def read_csv(path):
    if not path.exists():
        sys.exit(f"Datei nicht gefunden: {path}\nBitte Dateiname oder Pfad im Skript prüfen.")
    for enc in ("utf-8-sig", "cp1252", "latin1"):
        try:
            return pd.read_csv(path, sep=None, engine="python", encoding=enc)
        except (UnicodeError, pd.errors.ParserError, ValueError):
            continue
    sys.exit(f"CSV konnte nicht gelesen werden: {path}")


def canon(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def column(df, *aliases):
    lookup = {canon(c): c for c in df.columns}
    for alias in aliases:
        if canon(alias) in lookup:
            return lookup[canon(alias)]
    return None


def normalize_values(series):
    s = series.astype("string").str.strip()
    return s.mask(s.str.lower().isin(["", "nan", "none", "null", "nat"]))


def print_section(title):
    print("\n" + "=" * 72 + "\n" + title + "\n" + "=" * 72)


def size_table(df, keys, name):
    g = (df.dropna(subset=keys).groupby(keys, dropna=False, observed=True)
         .size().rename("n").reset_index().sort_values("n", ascending=False))
    g.to_csv(OUT / f"gruppen_{name}.csv", index=False, encoding="utf-8-sig")
    print(f"\n{name}: {len(g)} Gruppen; abgedeckte Incidents: {int(g.n.sum()):,}")
    print(g.head(15).to_string(index=False))
    for threshold in MIN_SIZES:
        print(f"  Gruppen mit >= {threshold} Fällen: {(g.n >= threshold).sum()} "
              f"(Incidents in diesen Gruppen: {int(g.loc[g.n >= threshold, 'n'].sum()):,})")
    if "duration_h" in df.columns:
        stats = (df.dropna(subset=keys).groupby(keys, observed=True)["duration_h"]
                 .agg(n_duration="count", median_h="median",
                      q25_h=lambda x: x.quantile(.25),
                      q75_h=lambda x: x.quantile(.75))
                 .reset_index())
        stats["iqr_h"] = stats["q75_h"] - stats["q25_h"]
        stats.to_csv(OUT / f"dauer_{name}.csv", index=False, encoding="utf-8-sig")
    return g


def main():
    OUT.mkdir(exist_ok=True)
    incident = read_csv(INCIDENT)
    activity = read_csv(ACTIVITY)
    print_section("1. Datenbasis")
    print(f"Incidents: {len(incident):,} Zeilen, {len(incident.columns)} Spalten")
    print(f"Activities: {len(activity):,} Zeilen, {len(activity.columns)} Spalten")
    print("\nIncident-Spalten:\n" + "\n".join(map(str, incident.columns)))
    print("\nActivity-Spalten:\n" + "\n".join(map(str, activity.columns)))

    id_inc = column(incident, "Incident ID", "IncidentID", "Incident Number")
    id_act = column(activity, "Incident ID", "IncidentID", "Incident Number")
    priority = column(incident, "Priority", "Priority Name")
    category = column(incident, "Category", "Category Name", "Incident Category")
    opened = column(incident, "Open Time", "Opened Time", "Opened At", "Open Date", "Opened")
    resolved = column(incident, "Resolved Time", "Resolution Time", "Resolved At", "Resolve Time")
    closed = column(incident, "Close Time", "Closed Time", "Closed At", "Closure Time")
    print_section("2. Erkannte Schlüsselfelder")
    for label, value in [("Incident-ID", id_inc), ("Activity-Incident-ID", id_act),
                         ("Priority", priority), ("Category", category),
                         ("Open Time", opened), ("Resolved Time", resolved), ("Close Time", closed)]:
        print(f"{label:22}: {value or 'NICHT GEFUNDEN'}")

    if id_inc:
        print(f"\nDoppelte Incident-IDs in Incident-Datei: {incident[id_inc].duplicated().sum():,}")
    if id_inc and id_act:
        inc_ids = set(normalize_values(incident[id_inc]).dropna())
        act_ids = normalize_values(activity[id_act])
        print(f"Activities mit passender Incident-ID: {act_ids.isin(inc_ids).sum():,} / {len(activity):,}")
        counts = act_ids.value_counts(dropna=True)
        print(f"Median Activities pro Incident (mit Activity): {counts.median():.1f}")
        counts.rename_axis("Incident_ID").reset_index(name="activities").to_csv(
            OUT / "aktivitaeten_pro_incident.csv", index=False, encoding="utf-8-sig")

    if not priority or not category:
        print("\nACHTUNG: Priority oder Category nicht automatisch erkannt. "
              "Bitte die ausgegebenen Spaltennamen prüfen.")
    if priority:
        incident["priority_group"] = normalize_values(incident[priority])
    if category:
        incident["category_group"] = normalize_values(incident[category])

    end = resolved or closed
    if opened and end:
        op = pd.to_datetime(incident[opened], errors="coerce", dayfirst=True)
        en = pd.to_datetime(incident[end], errors="coerce", dayfirst=True)
        incident["duration_h"] = (en - op).dt.total_seconds() / 3600
        incident.loc[incident["duration_h"] < 0, "duration_h"] = np.nan
        print_section("3. Bearbeitungsdauer (Open → Resolved/Close)")
        print(f"Verwendete Spalten: {opened} → {end}")
        print(f"Gültige Dauern: {incident.duration_h.notna().sum():,} / {len(incident):,}")
        print(incident.duration_h.describe(percentiles=[.25,.5,.75,.9,.95,.99]).round(2))
        print("Hinweis: Zeitstempel-Parsing und fachliche Bedeutung vor endgültiger Analyse prüfen.")
    else:
        print("\nBearbeitungsdauer nicht berechnet; passende Zeitspalten nicht erkannt.")

    print_section("4. Kontextgruppen und Stichprobengrößen")
    if priority:
        print(f"Fehlende Priority: {incident.priority_group.isna().sum():,}")
        size_table(incident, ["priority_group"], "priority")
    if category:
        print(f"Fehlende Category: {incident.category_group.isna().sum():,}")
        size_table(incident, ["category_group"], "category")
    if priority and category:
        size_table(incident, ["priority_group", "category_group"], "priority_category")

    print_section("5. Fazit für die Machbarkeitsprüfung")
    print(f"CSV-Ergebnisdateien: {OUT}")
    print("Die Mindestgrößen sind rein explorativ: Für Experiment B sind zusätzlich "
          "zurückgehaltene Testfälle je Gruppe notwendig.")
    print("Als Nächstes: Gruppengrößen, fehlende Werte und Dauerverteilungen fachlich prüfen.")


if __name__ == "__main__":
    main()
