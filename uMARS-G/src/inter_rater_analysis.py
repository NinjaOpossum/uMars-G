import pandas as pd
from pingouin import intraclass_corr
import os

base_output_dir = r'C:\Users\manue\OneDrive - ges.thm.de\THMmaster\Semester 1\EHealth\uMARS-G\src\output'

def calculate_inter_rater_icc(data_frames, section_name, rater_ids):
    # Kombinieren der Datenframes mit den Rater-IDs als Rater-Spalte
    combined_df = pd.concat(data_frames, keys=rater_ids).reset_index()
    combined_df = combined_df.rename(columns={'level_0': 'Rater', 'level_1': 'index', 0: 'value'})
    
    combined_df = combined_df.dropna(subset=['value'])
    
    if combined_df.empty:
        print(f"Keine gültigen Daten für {section_name}. Überspringen...")
        return None
    
    icc_results = intraclass_corr(data=combined_df, targets='index', raters='Rater', ratings='value', nan_policy='omit')
    print(f"Intraclass Correlation Coefficient (ICC) für {section_name} (Inter-Rater):")
    print(icc_results[['Type', 'ICC', 'CI95%']])
    
    # Rückgabe der ICC-Ergebnisse
    icc_results['Section'] = section_name
    return icc_results[['Section', 'Type', 'ICC', 'CI95%']]

def save_inter_rater_icc(all_icc_results, rater_ids):
    output_dir = os.path.join(base_output_dir, 'inter', 'icc')
    os.makedirs(output_dir, exist_ok=True)
    filename = f"Rater_{'_'.join(map(str, rater_ids))}_inter_icc_results.csv"
    output_path = os.path.join(output_dir, filename)
    all_icc_results.to_csv(output_path, index=False)
    print(f"Alle Inter-Rater ICC Ergebnisse gespeichert unter: {output_path}")

def analyze_inter_rater(data_frames, rater_ids):
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
        section_dfs = [df.iloc[:, cols] for df in data_frames]
        
        for df in section_dfs:
            df.columns = [f"{section_name}_{i}" for i in range(1, len(cols) + 1)]
            df = df.apply(pd.to_numeric, errors='coerce')

        icc_result = calculate_inter_rater_icc(section_dfs, section_name, rater_ids)
        if icc_result is not None:
            all_icc_results = pd.concat([all_icc_results, icc_result], ignore_index=True)

    if not all_icc_results.empty:
        save_inter_rater_icc(all_icc_results, rater_ids)
