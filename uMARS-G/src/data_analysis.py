import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pingouin import intraclass_corr
import os
import shutil

# Hauptausgabeverzeichnis initialisieren
base_output_dir = r'C:\Users\manue\OneDrive - ges.thm.de\THMmaster\Semester 1\EHealth\uMARS-G\src\output'
os.makedirs(base_output_dir, exist_ok=True)

def sanitize_sheet_name(sheet_name):
    # Entferne ungültige Zeichen und kürze den Namen auf 31 Zeichen
    sanitized_name = sheet_name.replace(":", "").replace(" ", "_").replace("/", "_").replace("\\", "_").replace("?", "").replace("*", "").replace("[", "").replace("]", "")
    return sanitized_name[:31]

def calculate_icc(df1, df2, section_name, rater_id):
    df_combined = pd.concat([df1, df2], keys=['Runde1', 'Runde2']).reset_index()
    df_combined = df_combined.rename(columns={'level_0': 'Runde', 'level_1': 'index', 0: 'value'})
    
    df_combined = df_combined.dropna(subset=['value'])
    
    if df_combined.empty:
        print(f"Keine gültigen Daten für {section_name}. Überspringen...")
        return None
    
    icc_results = intraclass_corr(data=df_combined, targets='index', raters='Runde', ratings='value', nan_policy='omit')
    print(f"Intraclass Correlation Coefficient (ICC) für {section_name}:")
    print(icc_results[['Type', 'ICC', 'CI95%']])
    
    # Rückgabe der ICC-Ergebnisse
    icc_results['Section'] = section_name
    return icc_results[['Section', 'Type', 'ICC', 'CI95%']]

def save_icc_to_csv(all_icc_results, rater_id, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"Rater{rater_id}_icc_results.csv"
    output_path = os.path.join(output_dir, filename)
    all_icc_results.to_csv(output_path, index=False)
    print(f"Alle ICC Ergebnisse gespeichert unter: {output_path}")

def save_dataframes_to_excel(data_frames, rater_id):
    output_dir = r'C:\Users\manue\OneDrive - ges.thm.de\THMmaster\Semester 1\EHealth\uMARS-G\src\output\intra\dataframes'
    os.makedirs(output_dir, exist_ok=True)
    filename = f"Rater{rater_id}_dataframes.xlsx"
    output_path = os.path.join(output_dir, filename)

    with pd.ExcelWriter(output_path) as writer:
        df1 = data_frames[0]
        df2 = data_frames[1]

        sections = {
            "SECTION A: Engagement": list(range(1, 6)),
            "SECTION B: Funktionalität": list(range(6, 10)),
            "SECTION C: Ästhetik": list(range(10, 13)),
            "SECTION D: Information": list(range(13, 17)),
            "SECTION E: Subjektive Qualität der App": list(range(17, 21)),
            "SECTION F: Wahrgenommene Wirkung der App": list(range(21, 27))
        }

        for section_name, cols in sections.items():
            section_df1 = df1.iloc[:, cols]
            section_df2 = df2.iloc[:, cols]

            section_df1.columns = [f"{section_name}_Runde1_{i}" for i in range(1, len(cols) + 1)]
            section_df2.columns = [f"{section_name}_Runde2_{i}" for i in range(1, len(cols) + 1)]

            combined_df = pd.concat([section_df1, section_df2], axis=1)
            sanitized_sheet_name = sanitize_sheet_name(section_name)
            combined_df.to_excel(writer, sheet_name=sanitized_sheet_name)

    print(f"Die DataFrames wurden erfolgreich unter {output_path} gespeichert.")

import os
import pandas as pd

def analyze_intra_rater(data_frames, method, rater_id):
    if len(data_frames) < 2:
        print("Für die Intra-Rater-Analyse werden mindestens zwei Bewertungsrunden benötigt.")
        return
    
    df1 = data_frames[0]
    df2 = data_frames[1]

    sections = {
        "SECTION A: Engagement": list(range(1, 6)),
        "SECTION B: Funktionalität": list(range(6, 10)),
        "SECTION C: Ästhetik": list(range(10, 13)),
        "SECTION D: Information": list(range(13, 17)),
        "SECTION E: Subjektive Qualität der App": list(range(17, 21)),
        "SECTION F: Wahrgenommene Wirkung der App": list(range(21, 27))
    }
    
    all_icc_results = pd.DataFrame()

    for section_name, cols in sections.items():
        section_df1 = df1.iloc[:, cols]
        section_df2 = df2.iloc[:, cols]

        section_df1.columns = [f"{section_name}_{i}" for i in range(1, len(cols) + 1)]
        section_df2.columns = [f"{section_name}_{i}" for i in range(1, len(cols) + 1)]

        section_df1 = section_df1.apply(pd.to_numeric, errors='coerce')
        section_df2 = section_df2.apply(pd.to_numeric, errors='coerce')

        section_df1_mean = section_df1.mean(axis=1)
        section_df2_mean = section_df2.mean(axis=1)

        if method == '1':
            icc_result = calculate_icc(section_df1_mean, section_df2_mean, section_name, rater_id)
            if icc_result is not None:
                all_icc_results = pd.concat([all_icc_results, icc_result], ignore_index=True)
        elif method == '2':
            # Boxplot wird hier nur einmalig pro Sektion generiert
            boxplot_comparison(section_df1_mean, section_df2_mean, section_name)
        elif method == '4':
            # Nur die DataFrames speichern, keine ICC-Berechnungen
            save_dataframes_to_excel(data_frames, rater_id)

    if method == '1' and not all_icc_results.empty:
        output_dir = os.path.join(base_output_dir, 'intra', 'icc')
        save_icc_to_csv(all_icc_results, rater_id, output_dir)


def boxplot_comparison(df1, df2, section_name):
    df1 = pd.DataFrame({'Bewertungen': df1, 'Runde': 'Runde 1'}).reset_index(drop=True)
    df2 = pd.DataFrame({'Bewertungen': df2, 'Runde': 'Runde 2'}).reset_index(drop=True)
    
    combined_df = pd.concat([df1, df2]).reset_index(drop=True)
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Runde', y='Bewertungen', data=combined_df)
    plt.xlabel('Runde')
    plt.ylabel('Bewertungen')
    plt.title(f'Boxplot Vergleich: {section_name}')
    plt.show()

def rank_apps_with_changes(data_frames):
    rankings = []

    for i, df in enumerate(data_frames):
        df = df.dropna()
        df_numeric = df.iloc[:, 1:-2].apply(pd.to_numeric, errors='coerce')
        df_numeric.index = df.iloc[:, 0]

        app_means = df_numeric.mean(axis=1)
        ranking = app_means.sort_values(ascending=False)
        rankings.append(ranking)
        print(f"Ranking der Apps für Runde {i+1}:")
        print(ranking)

    combined_ranking = pd.DataFrame(rankings).T
    combined_ranking.columns = [f'Runde {i+1}' for i in range(len(data_frames))]

    if len(data_frames) > 1:
        combined_df = pd.concat(data_frames, axis=0)
        combined_df = combined_df.dropna(subset=[combined_df.columns[0]])
        
        combined_df_numeric = combined_df.iloc[:, 1:-2].apply(pd.to_numeric, errors='coerce')
        combined_df_numeric.index = combined_df.iloc[:, 0]

        combined_means = combined_df_numeric.groupby(combined_df_numeric.index).mean()
        combined_means = combined_means.mean(axis=1)
        combined_ranking['Kombiniert'] = combined_means.sort_values(ascending=False)

        combined_ranking['Change'] = combined_ranking.apply(
            lambda row: get_change_indicator(row), axis=1
        )

        print("Kombiniertes Ranking der Apps für alle Runden:")
        print(combined_ranking)

        generate_ranking_image(combined_ranking)

        # Bild verschieben
        output_dir = os.path.join(base_output_dir, 'app_rankings')
        os.makedirs(output_dir, exist_ok=True)
        src = 'app_rankings_with_changes.png'
        dst = os.path.join(output_dir, 'app_rankings_with_changes.png')
        shutil.move(src, dst)
        print(f"Bild wurde verschoben nach {dst}")
    rankings = []

    for i, df in enumerate(data_frames):
        df = df.dropna()
        df_numeric = df.iloc[:, 1:-2].apply(pd.to_numeric, errors='coerce')
        df_numeric.index = df.iloc[:, 0]

        app_means = df_numeric.mean(axis=1)
        ranking = app_means.sort_values(ascending=False)
        rankings.append(ranking)
        print(f"Ranking der Apps für Runde {i+1}:")
        print(ranking)

    combined_ranking = pd.DataFrame(rankings).T
    combined_ranking.columns = [f'Runde {i+1}' for i in range(len(data_frames))]

    if len(data_frames) > 1:
        combined_df = pd.concat(data_frames, axis=0)
        combined_df = combined_df.dropna(subset=[combined_df.columns[0]])
        
        combined_df_numeric = combined_df.iloc[:, 1:-2].apply(pd.to_numeric, errors='coerce')
        combined_df_numeric.index = combined_df.iloc[:, 0]

        combined_means = combined_df_numeric.groupby(combined_df_numeric.index).mean()
        combined_means = combined_means.mean(axis=1)
        combined_ranking['Kombiniert'] = combined_means.sort_values(ascending=False)

        combined_ranking['Change'] = combined_ranking.apply(
            lambda row: get_change_indicator(row), axis=1
        )

        print("Kombiniertes Ranking der Apps für alle Runden:")
        print(combined_ranking)

        generate_ranking_image(combined_ranking)

        # Bild verschieben
        output_dir = os.path.join(base_output_dir, 'app_rankings')
        os.makedirs(output_dir, exist_ok=True)
        src = 'app_rankings_with_changes.png'
        dst = os.path.join(output_dir, 'app_rankings_with_changes.png')
        shutil.move(src, dst)
        print(f"Bild wurde verschoben nach {dst}")

def get_change_indicator(row):
    if len(row) < 3:
        return ''
    
    change = row[-2] - row[0]
    if change < 0:
        return '🟢↑'  # Green up arrow for improvement
    elif change > 0:
        return '🔴↓'  # Red down arrow for decline
    else:
        return '➖'  # Gray right arrow for no change

def generate_ranking_image(combined_ranking):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    table = ax.table(cellText=combined_ranking.values, colLabels=combined_ranking.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    file_path = 'app_rankings_with_changes.png'
    plt.savefig(file_path)
    plt.close()
    print(f"Das Bild wurde als '{file_path}' gespeichert.")

def rank_apps_with_changes(data_frames):
    rankings = []

    for i, df in enumerate(data_frames):
        df = df.dropna()
        df_numeric = df.iloc[:, 1:-2].apply(pd.to_numeric, errors='coerce')
        df_numeric.index = df.iloc[:, 0]

        app_means = df_numeric.mean(axis=1)
        ranking = app_means.sort_values(ascending=False)
        rankings.append(ranking)
        print(f"Ranking der Apps für Runde {i+1}:")
        print(ranking)

    combined_ranking = pd.DataFrame(rankings).T
    combined_ranking.columns = [f'Runde {i+1}' for i in range(len(data_frames))]

    if len(data_frames) > 1:
        combined_df = pd.concat(data_frames, axis=0)
        combined_df = combined_df.dropna(subset=[combined_df.columns[0]])
        
        combined_df_numeric = combined_df.iloc[:, 1:-2].apply(pd.to_numeric, errors='coerce')
        combined_df_numeric.index = combined_df.iloc[:, 0]

        combined_means = combined_df_numeric.groupby(combined_df_numeric.index).mean()
        combined_means = combined_means.mean(axis=1)
        combined_ranking['Kombiniert'] = combined_means.sort_values(ascending=False)

        combined_ranking['Change'] = combined_ranking.apply(
            lambda row: get_change_indicator(row), axis=1
        )

        print("Kombiniertes Ranking der Apps für alle Runden:")
        print(combined_ranking)

        generate_ranking_image(combined_ranking)

        # Bild verschieben
        output_dir = r'C:\Users\manue\OneDrive - ges.thm.de\THMmaster\Semester 1\EHealth\uMARS-G\src\output'
        os.makedirs(output_dir, exist_ok=True)
        src = 'app_rankings_with_changes.png'
        dst = os.path.join(output_dir, 'app_rankings_with_changes.png')
        shutil.move(src, dst)
        print(f"Bild wurde verschoben nach {dst}")

def move_image():
    src = 'app_rankings_with_changes.png'
    dst = r'C:\Users\manue\OneDrive - ges.thm.de\THMmaster\Semester 1\EHealth\uMARS-G\src\output\app_rankings_with_changes.png'
    shutil.move(src, dst)
    print(f"Bild wurde verschoben nach {dst}")
