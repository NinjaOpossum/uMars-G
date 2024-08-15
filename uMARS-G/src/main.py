import os
import pandas as pd
from file_operations import get_excel_files, load_excel_files, save_data_frames, load_existing_files, remove_total_columns
from data_analysis import analyze_intra_rater, generate_ranking_image, rank_apps_with_changes, save_dataframes_to_excel, save_icc_to_csv
from utils import get_analysis_type, get_rater_id, get_analysis_method
from inter_rater_analysis import analyze_inter_rater

def get_missing_rater_ids(rater_ids, data_frames):
    loaded_rater_ids = set()
    for df in data_frames:
        if 'RaterId' in df.columns:
            loaded_rater_ids.add(str(df['RaterId'].iloc[0]))
        else:
            print(f"RaterId konnte in einer Datei nicht gefunden werden.")
    
    input_rater_ids = set(rater_ids.split(','))

    print(f"Geladene Rater-IDs: {loaded_rater_ids}")
    missing_rater_ids = input_rater_ids - loaded_rater_ids
    return list(missing_rater_ids)



def assign_rater_id_to_data(rater_id, data_frames):
    assigned_data = []
    for i, df in enumerate(data_frames):
        df['RaterId'] = rater_id
        df['Runde'] = i + 1
        assigned_data.append(df)
    return assigned_data

def main():
    analysis_type = get_analysis_type()
    rater_id = get_rater_id(analysis_type)

    if analysis_type == 'INTER' and len(rater_id.split(',')) < 2:
        print("Für eine Inter-Rater-Analyse müssen mindestens zwei Rater-IDs angegeben werden.")
        return

    # Versuche, bestehende Dateien zu laden
    data_frames = load_existing_files(rater_id)
    original_filenames = [f"bewertung_rater_{rater}_runde_{i+1}.xlsx" for rater in rater_id.split(',') for i in range(2)]  # Example filenames
    
    # Überprüfen, ob für alle Rater IDs Dateien geladen wurden, ansonsten nach den fehlenden Dateien fragen
    missing_rater_ids = get_missing_rater_ids(rater_id, data_frames)

    while missing_rater_ids:
        print(f"Für folgende Rater-IDs fehlen Dateien: {', '.join(missing_rater_ids)}")
        excel_files = get_excel_files()
        if not excel_files:
            print("Keine Dateien zum Laden. Bitte stellen Sie sicher, dass Sie die fehlenden Dateien hochladen.")
            return
        
        # Lade die neuen Dateien und füge sie den vorhandenen DataFrames hinzu
        new_data_frames = load_excel_files(excel_files)
        data_frames.extend(new_data_frames)
        
        # Füge die originalen Dateinamen der Liste hinzu
        original_filenames.extend(excel_files)

        # Speichern der neuen Dateien mit ihren ursprünglichen Namen
        save_data_frames(new_data_frames, original_filenames)
        
        # Aktualisiere die Liste der fehlenden Rater-IDs nach dem Laden neuer Dateien
        missing_rater_ids = get_missing_rater_ids(rater_id, data_frames)

    assigned_data = data_frames

    while True:
        method = get_analysis_method()

        if analysis_type == 'INTRA':
            if method == '1':  # Method 1 for ICC
                print(f"Intra-Rater Analyse wird durchgeführt für Rater ID: {rater_id}")
                analyze_intra_rater(assigned_data, method, rater_id)
            elif method == '2':  # Method 2 for Boxplot Comparison
                analyze_intra_rater(assigned_data, method, rater_id)
            elif method == '3':  # Method 3 for Ranking
                rank_apps_with_changes(assigned_data)
            elif method == '4':  # Method 4 for Debug: Save DataFrames and ICC results
                print(f"Speichern der DataFrames und ICC-Ergebnisse für Rater ID: {rater_id}")
                save_dataframes_to_excel(assigned_data, rater_id)
                analyze_intra_rater(assigned_data, '1', rater_id)  # Berechnung der ICC-Ergebnisse
                save_icc_to_csv(pd.DataFrame(), rater_id, os.path.join('output', 'intra', 'icc'))
        elif analysis_type == 'INTER':
            if method == '1':  # Method 1 for Inter-Rater ICC
                print(f"Inter-Rater Analyse wird durchgeführt für die Rater IDs: {rater_id}")
                analyze_inter_rater(assigned_data, rater_id.split(','))

        another_analysis = input("Möchten Sie eine weitere Analyse durchführen? (ja/nein): ").strip().lower()

        if another_analysis != 'ja':
            break

if __name__ == "__main__":
    main()

