import pandas as pd
import pingouin as pg

def load_data(filepath):
    """Lädt die Daten aus einer CSV-Datei und konvertiert relevante Spalten in numerische Werte."""
    df = pd.read_csv(filepath)

    # Liste der Spalten, die in numerische Werte konvertiert werden sollen
    numerical_columns = [
        'Unterhaltung', 'Interesse', 'Individuelle Anpassbarkeit', 'Interaktivität', 'Zielgruppe',
        'SECTION A: Engagement', 'Leistung', 'Nutzerfreundlichkeit', 'Navigation', 'Motorisches, gestisches Design',
        'SECTION B: Funktionalität', 'Layout', 'Grafik', 'Visueller Anreiz', 'SECTION C: Ästhetik',
        'Qualität der Information', 'Quantität der Information', 'Visuelle Information', 'Glaubwürdigkeit',
        'SECTION D: Information', 'Bewusstsein', 'Wissen', 'Einstellung', 'Absicht zur Veränderung',
        'Hilfe suchen', 'Verhaltensänderung', 'SECTION F: Wahrgenommene Wirkung der App'
    ]

    # Konvertiere Spalten in numerische Werte und setze nicht-konvertierbare Werte auf NaN
    for col in numerical_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def calculate_icc(data):
    """Berechnet die ICC für alle Variablen und alle Apps, basierend auf den Datenwerten."""
    variables = [
        'Unterhaltung', 'Interesse', 'Individuelle Anpassbarkeit', 'Interaktivität', 'Zielgruppe',
        'SECTION A: Engagement', 'Leistung', 'Nutzerfreundlichkeit', 'Navigation', 'Motorisches, gestisches Design',
        'SECTION B: Funktionalität', 'Layout', 'Grafik', 'Visueller Anreiz', 'SECTION C: Ästhetik',
        'Qualität der Information', 'Quantität der Information', 'Visuelle Information', 'Glaubwürdigkeit',
        'SECTION D: Information', 'Bewusstsein', 'Wissen', 'Einstellung', 'Absicht zur Veränderung',
        'Hilfe suchen', 'Verhaltensänderung', 'SECTION F: Wahrgenommene Wirkung der App'
    ]
    
    icc_results = []

    # Berechne die ICC für jede App und jede Variable
    for app_name in data['App_Name'].unique():
        app_data = data[data['App_Name'] == app_name]

        for variable in variables:
            icc_data = app_data[['Rater', variable]].dropna()  # Entfernen von Zeilen mit fehlenden Daten
            print(f"Verarbeite App: {app_name}, Variable: {variable}, verfügbare Zeilen: {len(icc_data)}")  # Debugging-Ausgabe
            
            if len(icc_data) < 5:
                print(f"Nicht genügend Daten für die Variable {variable} und App {app_name}. Überspringen.")
                continue

            try:
                # Umwandeln in langes Format
                icc_data_long = icc_data.reset_index().melt(id_vars='Rater', var_name='Variable', value_name='Score')
                icc_data_long.rename(columns={'Rater': 'Subject'}, inplace=True)

                # Berechnung der ICC für die aktuelle Variable
                icc = pg.intraclass_corr(data=icc_data_long, targets='Subject', raters='Variable', ratings='Score', nan_policy='omit')
                
                # Berechne ICC(2,k), ICC(3,k) und ICC(3,1)
                icc_2k_value = icc[icc['Type'] == 'ICC2k']
                icc_3k_value = icc[icc['Type'] == 'ICC3k']
                icc_31_value = icc[icc['Type'] == 'ICC3']

                icc_results.append({
                    'Appname': app_name,
                    'Variable': variable,
                    'ICC(2,k) Interrater': icc_2k_value['ICC'].values[0] if not icc_2k_value.empty else None,
                    'ICC(2,k) 95 conf': icc_2k_value['CI95%'].values[0] if not icc_2k_value.empty else None,
                    'ICC(3,k) Interrater': icc_3k_value['ICC'].values[0] if not icc_3k_value.empty else None,
                    'ICC(3,k) 95 conf': icc_3k_value['CI95%'].values[0] if not icc_3k_value.empty else None,
                    'ICC(3,1) Interrater': icc_31_value['ICC'].values[0] if not icc_31_value.empty else None,
                    'ICC(3,1) 95 conf': icc_31_value['CI95%'].values[0] if not icc_31_value.empty else None,
                })
            except ValueError as e:
                print(f"Ein Fehler trat auf bei der Verarbeitung der Variable {variable} für App {app_name}: {e}")
                continue

    # Ausgabe der Ergebnisse
    if icc_results:
        print("ICC-Ergebnisse erfolgreich berechnet.")
        return icc_results
    else:
        print("Keine ICC-Ergebnisse verfügbar.")
        return None

def main():
    # Daten laden
    data = load_data('raters1.csv')  # Stelle sicher, dass der Pfad korrekt ist

    # ICC-Ergebnisse berechnen
    final_results = calculate_icc(data)

    # Wenn Ergebnisse vorhanden sind, speichere sie in einer CSV-Datei
    if final_results:
        results_df = pd.DataFrame(final_results)
        print(results_df.head())  # Zeige die ersten Zeilen für Debugging

        # Ergebnisse in CSV-Datei speichern
        results_df.to_csv('icc_results2.csv', index=False, sep=';')
        print("Ergebnisse wurden in icc_results.csv gespeichert.")
    else:
        print("Keine Ergebnisse zu speichern.")

if __name__ == "__main__":
    main()
