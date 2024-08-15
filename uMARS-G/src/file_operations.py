import os
import pandas as pd
import re

def normalize_path(file_path):
    return os.path.normpath(file_path.strip().strip('"'))

def get_excel_files():
    files = []
    while True:
        file_path = input("Bitte geben Sie den Pfad zur Excel-Datei ein. HINWEIS: Laden Sie mindestens eine Excel-Datei hoch, es können aber auch mehrere Dateien für Vergleiche hochgeladen werden. Beenden Sie Ihre Pfad-Eingabe mit 'done': ").strip()
        if file_path.lower() == 'done':
            break
        normalized_path = normalize_path(file_path)
        print(f"Überprüfe Pfad: {normalized_path}")
        if os.path.isfile(normalized_path):
            files.append(normalized_path)
            print(f"Datei gefunden: {normalized_path}")
        else:
            print("Datei nicht gefunden. Bitte geben Sie einen gültigen Pfad ein.")
    return files

def load_excel_files(files, rater_id=None):
    data_frames = []
    for file in files:
        try:
            df = pd.read_excel(file, header=0)
            extracted_rater_id = extract_rater_id_from_filename(os.path.basename(file))
            if 'RaterId' not in df.columns:
                rater_id = extracted_rater_id if rater_id is None else rater_id
                df['RaterId'] = rater_id
            print(f"Geladene RaterId für Datei {os.path.basename(file)}: {df['RaterId'].iloc[0]}")
            data_frames.append(df)
            print(f"Erfolgreich geladen: {file}")
        except Exception as e:
            print(f"Fehler beim Laden der Datei {file}: {e}")
    return data_frames


def save_data_frames(data_frames, original_filenames):
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for df, original_filename in zip(data_frames, original_filenames):
        base_name = os.path.basename(original_filename)
        parts = base_name.split('_')
        
        try:
            rater_id = parts[2]  # Annahme: Rater ID ist der dritte Teil im Dateinamen
            round_number = parts[3].replace(".xlsx", "")  # Annahme: Runde ist der vierte Teil im Dateinamen
        except IndexError:
            rater_id = extract_rater_id_from_filename(base_name)
            round_number = "Unbekannt"

        # Setze die RaterId und Runde in das DataFrame ein, falls diese Spalten fehlen
        if 'RaterId' not in df.columns:
            print("RaterId-Spalte fehlt. Sie wird automatisch hinzugefügt.")
            df['RaterId'] = rater_id

        if 'Runde' not in df.columns:
            df['Runde'] = round_number

        output_file = os.path.join(output_dir, base_name)
        df.to_excel(output_file, index=False)
        print(f"Gespeichert: {output_file}")


def load_existing_files(rater_id, input_dir="data"):
    data_frames = []
    rater_ids = rater_id.split(',')

    for rater in rater_ids:
        found_files = False
        for file_name in os.listdir(input_dir):
            if file_name.startswith(f"bewertung_rater_{rater}_"):
                try:
                    df = pd.read_excel(os.path.join(input_dir, file_name), header=0)
                    if 'RaterId' in df.columns:
                        print(f"Geladene RaterId für Datei {file_name}: {df['RaterId'].iloc[0]}")
                    else:
                        print(f"RaterId-Spalte fehlt in der Datei {file_name}")
                    data_frames.append(df)
                    print(f"Erfolgreich geladen: {os.path.join(input_dir, file_name)}")
                    found_files = True
                except Exception as e:
                    print(f"Fehler beim Laden der Datei {file_name}: {e}")
        if not found_files:
            print(f"Keine Dateien für Rater ID {rater} gefunden. Bitte die entsprechenden Dateien hochladen.")

    return data_frames


def remove_total_columns(data_frames):
    total_columns_indices = [6, 11, 15, 20, 25, 32]  # Zero-based index for columns 7, 12, 16, 21, 26, 33
    cleaned_data_frames = []
    for df in data_frames:
        # Filter out indices that are out of bounds
        valid_indices = [idx for idx in total_columns_indices if idx < df.shape[1]]
        cleaned_df = df.drop(df.columns[valid_indices], axis=1)
        cleaned_data_frames.append(cleaned_df)
    return cleaned_data_frames

def show_section_data(file_path, section_name, section_range):
    try:
        df = pd.read_excel(file_path, header=0)
        section_columns = df.columns[section_range[0]:section_range[-1] + 1]
        
        print(f"Spalten für {section_name}:")
        print(section_columns)
        
        print(f"Daten für {section_name}:")
        print(df[section_columns].head())
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")

def extract_rater_id_from_filename(filename):
    # Annahme: Die Rater-ID ist eine Zahl, die im Dateinamen vorkommt und von Unterstrichen umgeben ist, z.B. _29_
    match = re.search(r'_([0-9]+)_', filename)
    if match:
        return match.group(1)
    else:
        return "Unbekannt"
