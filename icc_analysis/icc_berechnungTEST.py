import pandas as pd
import pingouin as pg

def berechne_icc():
    # Liste der Items (Variablen)
    items = [
        'Unterhaltung', 'Interesse', 'IndividuelleAnpassbarkeit', 'Interaktivität',
        'Zielgruppe', 'Engagement', 'Leistung', 'Nutzerfreundlichkeit',
        'Navigation', 'MotorischesDesign', 'Funktionalität',
        'Layout', 'Grafik', 'VisuellerAnreiz', 'Ästhetik',
        'QualitätInformation', 'QuantitätInformation', 'VisuelleInformation',
        'Glaubwürdigkeit', 'Bewusstsein', 'Wissen',
        'Einstellung', 'AbsichtZurVeränderung', 'HilfeSuchen', 'Verhaltensänderung',
        'WahrgenommeneWirkung'
    ]

    data = {
        'Person': [1, 2, 3, 4, 5],
        'Rater1_Unterhaltung': [85, 88, 90, 92, 91],
        'Rater2_Unterhaltung': [86, 87, 89, 91, 90],
        'Rater3_Unterhaltung': [84, 89, 88, 93, 92],
        'Rater1_Interesse': [70, 75, 80, 85, 90],
        'Rater2_Interesse': [72, 74, 82, 88, 89],
        'Rater3_Interesse': [73, 76, 81, 87, 91],
        'Rater1_IndividuelleAnpassbarkeit': [75, 77, 79, 82, 80],
        'Rater2_IndividuelleAnpassbarkeit': [76, 78, 80, 83, 81],
        'Rater3_IndividuelleAnpassbarkeit': [74, 79, 78, 85, 82],
        'Rater1_Interaktivität': [60, 62, 64, 66, 65],
        'Rater2_Interaktivität': [61, 63, 65, 67, 66],
        'Rater3_Interaktivität': [62, 64, 66, 68, 67],
        'Rater1_Zielgruppe': [88, 89, 91, 92, 90],
        'Rater2_Zielgruppe': [87, 88, 90, 91, 89],
        'Rater3_Zielgruppe': [89, 91, 90, 92, 91],
        'Rater1_Engagement': [82, 84, 85, 88, 87],
        'Rater2_Engagement': [83, 85, 86, 89, 88],
        'Rater3_Engagement': [81, 84, 86, 87, 89],
        'Rater1_Leistung': [79, 80, 81, 83, 84],
        'Rater2_Leistung': [80, 82, 84, 85, 83],
        'Rater3_Leistung': [81, 83, 85, 86, 82],
        'Rater1_Nutzerfreundlichkeit': [90, 91, 89, 88, 87],
        'Rater2_Nutzerfreundlichkeit': [89, 90, 88, 87, 86],
        'Rater3_Nutzerfreundlichkeit': [88, 89, 87, 86, 85],
        'Rater1_Navigation': [85, 87, 86, 88, 89],
        'Rater2_Navigation': [84, 86, 85, 87, 88],
        'Rater3_Navigation': [86, 88, 87, 89, 90],
        'Rater1_MotorischesDesign': [79, 81, 82, 84, 83],
        'Rater2_MotorischesDesign': [80, 82, 83, 85, 84],
        'Rater3_MotorischesDesign': [81, 83, 84, 86, 85],
        'Rater1_Funktionalität': [91, 92, 93, 90, 89],
        'Rater2_Funktionalität': [90, 91, 92, 89, 88],
        'Rater3_Funktionalität': [89, 90, 91, 88, 87],
        'Rater1_Layout': [87, 88, 89, 85, 84],
        'Rater2_Layout': [88, 89, 90, 86, 85],
        'Rater3_Layout': [89, 90, 91, 87, 86],
        'Rater1_Grafik': [83, 85, 86, 87, 84],
        'Rater2_Grafik': [82, 84, 85, 86, 83],
        'Rater3_Grafik': [81, 83, 84, 85, 82],
        'Rater1_VisuellerAnreiz': [88, 90, 91, 89, 87],
        'Rater2_VisuellerAnreiz': [87, 89, 90, 88, 86],
        'Rater3_VisuellerAnreiz': [89, 91, 92, 90, 88],
        'Rater1_Ästhetik': [85, 87, 89, 88, 90],
        'Rater2_Ästhetik': [84, 86, 88, 87, 89],
        'Rater3_Ästhetik': [86, 88, 90, 89, 91],
        'Rater1_QualitätInformation': [89, 90, 91, 92, 93],
        'Rater2_QualitätInformation': [88, 89, 90, 91, 92],
        'Rater3_QualitätInformation': [90, 91, 92, 93, 94],
        'Rater1_QuantitätInformation': [78, 79, 80, 81, 82],
        'Rater2_QuantitätInformation': [77, 78, 79, 80, 81],
        'Rater3_QuantitätInformation': [76, 77, 78, 79, 80],
        'Rater1_VisuelleInformation': [85, 86, 87, 88, 89],
        'Rater2_VisuelleInformation': [84, 85, 86, 87, 88],
        'Rater3_VisuelleInformation': [83, 84, 85, 86, 87],
        'Rater1_Glaubwürdigkeit': [92, 93, 94, 95, 96],
        'Rater2_Glaubwürdigkeit': [91, 92, 93, 94, 95],
        'Rater3_Glaubwürdigkeit': [90, 91, 92, 93, 94],
        'Rater1_Bewusstsein': [82, 84, 85, 86, 87],
        'Rater2_Bewusstsein': [83, 85, 86, 87, 88],
        'Rater3_Bewusstsein': [81, 83, 84, 85, 86],
        'Rater1_Wissen': [89, 90, 91, 92, 93],
        'Rater2_Wissen': [88, 89, 90, 91, 92],
        'Rater3_Wissen': [87, 88, 89, 90, 91],
        'Rater1_Einstellung': [70, 72, 74, 76, 78],
        'Rater2_Einstellung': [71, 73, 75, 77, 79],
        'Rater3_Einstellung': [72, 74, 76, 78, 80],
        'Rater1_AbsichtZurVeränderung': [85, 87, 88, 89, 90],
        'Rater2_AbsichtZurVeränderung': [84, 86, 87, 88, 89],
        'Rater3_AbsichtZurVeränderung': [83, 85, 86, 87, 88],
        'Rater1_HilfeSuchen': [91, 92, 93, 94, 95],
        'Rater2_HilfeSuchen': [90, 91, 92, 93, 94],
        'Rater3_HilfeSuchen': [89, 90, 91, 92, 93],
        'Rater1_Verhaltensänderung': [78, 79, 80, 81, 82],
        'Rater2_Verhaltensänderung': [77, 78, 79, 80, 81],
        'Rater3_Verhaltensänderung': [76, 77, 78, 79, 80],
        'Rater1_WahrgenommeneWirkung': [80, 82, 84, 86, 85],
        'Rater2_WahrgenommeneWirkung': [81, 83, 85, 87, 86],
        'Rater3_WahrgenommeneWirkung': [82, 84, 86, 88, 87]
    }

    df = pd.DataFrame(data)

    ergebnisse = []
    
    for item in items:
        print(f"Varianz für {item}:")
        print(df[[f'Rater1_{item}', f'Rater2_{item}', f'Rater3_{item}']].var())
        # Trennung der Daten für das aktuelle Item
        rater_columns = [f'Rater1_{item}', f'Rater2_{item}', f'Rater3_{item}']
        
        # Umwandeln in langes Format für das aktuelle Item
        df_long = df.melt(id_vars='Person', value_vars=rater_columns, 
                          var_name='Rater', value_name=item)
        df_long['Rater'] = df_long['Rater'].str.replace(f'_{item}', '')

        # ICC-Berechnungen
        icc_result = pg.intraclass_corr(data=df_long, targets='Person', raters='Rater', ratings=item)
        icc_2k = icc_result[icc_result['Type'] == 'ICC2k']
        icc_3k = icc_result[icc_result['Type'] == 'ICC3k']
        icc_31 = icc_result[icc_result['Type'] == 'ICC3']

        # Ergebnis formatieren
        ergebnisse.append({
            'Variable': item,
            'ICC(2,k) Interrater': icc_2k['ICC'].values[0] if not icc_2k.empty else None,
            'ICC(2,k) 95% conf': icc_2k['CI95%'].values[0] if not icc_2k.empty else None,
            'ICC(3,k) Interrater': icc_3k['ICC'].values[0] if not icc_3k.empty else None,
            'ICC(3,1) 95% conf': icc_31['CI95%'].values[0] if not icc_31.empty else None
        })

    # Ergebnisse in DataFrame formatieren und anzeigen
    ergebnisse_df = pd.DataFrame(ergebnisse)
    print(ergebnisse_df)

if __name__ == "__main__":
    berechne_icc()