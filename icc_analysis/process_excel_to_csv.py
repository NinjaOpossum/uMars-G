import pandas as pd

def load_excel_data(file_path):
    """Lädt die Excel-Datei und gibt ein DataFrame zurück."""

    # App Rating Google Play Store
    # df = pd.read_excel(file_path, sheet_name='App Rating Google Play Store')
    df = pd.read_excel(file_path, sheet_name='App Rating Apple App Store')
    return df

def process_excel_data(df):
    """Verarbeitet die Excel-Daten und erstellt die notwendige CSV."""
    # Wähle relevante Spalten aus
    columns_to_keep = [
        'App_Name', 'Rater', 'Messzeitpunkt', 'Unterhaltung', 'Interesse', 'Individuelle Anpassbarkeit', 
        'Interaktivität', 'Zielgruppe', 'SECTION A: Engagement', 'Leistung', 
        'Nutzerfreundlichkeit', 'Navigation', 'Motorisches, gestisches Design', 
        'SECTION B: Funktionalität', 'Layout', 'Grafik', 'Visueller Anreiz', 
        'SECTION C: Ästhetik', 'Qualität der Information', 'Quantität der Information', 
        'Visuelle Information', 'Glaubwürdigkeit', 'SECTION D: Information', 'Bewusstsein', 
        'Wissen', 'Einstellung', 'Absicht zur Veränderung', 'Hilfe suchen', 
        'Verhaltensänderung', 'SECTION F: Wahrgenommene Wirkung der App'
    ]
    # Stelle sicher, dass alle Spaltennamen korrekt sind
    missing_columns = [col for col in columns_to_keep if col not in df.columns]
    if missing_columns:
        print(f"Fehlende Spalten: {missing_columns}")
        return None  # Stoppe die Ausführung, wenn Spalten fehlen
    
    df = df[columns_to_keep]

    # Speichere das Ergebnis als CSV-Datei
    df.to_csv('uMARS-G_26_1.csv', index=False)

    return df

def main():
    # Pfad zur Excel-Datei
    file_path = 'uMARG-G_26_1.xlsx'
    
    # Daten laden
    df = load_excel_data(file_path)

    # Daten verarbeiten und CSV-Datei erstellen
    processed_df = process_excel_data(df)
    
    # Zeige das verarbeitete DataFrame an
    print(processed_df.head())

if __name__ == "__main__":
    main()
