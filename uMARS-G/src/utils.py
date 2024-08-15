import os

def normalize_path(file_path):
    return os.path.normpath(file_path.strip().strip('"'))

def get_analysis_type():
    while True:
        analysis_type = input("Möchten Sie eine INTRA oder INTER Rater Analyse durchführen? (INTRA/INTER): ").strip().upper()
        if analysis_type in ['INTRA', 'INTER']:
            return analysis_type
        print("Ungültige Eingabe. Bitte geben Sie 'INTRA' oder 'INTER' ein.")

def get_rater_id(analysis_type):
    if analysis_type == 'INTRA':
        return input("Bitte geben Sie die IntraRaterId ein: ").strip()
    elif analysis_type == 'INTER':
        return input("Bitte geben Sie die Rater IDs als Komma-getrennte Liste ein (z.B. 1,2,3): ").strip()


def get_analysis_method():
    while True:
        print("Wählen Sie eine statistische Methode:")
        print("1: Intraclass Correlation Coefficient (ICC)")
        print("2: Boxplot Vergleich")
        print("3: Ranking der Apps")
        print("4: Debug: Save DataFrame and ICC results")
        method = input("Bitte geben Sie die Nummer der gewünschten Methode ein (1/2/3/4): ").strip()
        if method in ['1', '2', '3', '4']:
            return method
        print("Ungültige Eingabe. Bitte geben Sie 1, 2, 3 oder 4 ein.")
