import random

SEED = 1234
random.seed(SEED)

from wczytywanie_danych import wczytaj_umiejetnosci, wczytaj_rozklad_zajec, wczytaj_dyspozycyjnosc, wczytaj_kalendarz, wczytaj_rozklad_zajec_miesiac
from walidacja_danych import waliduj_df
from generowanie_harmonogramu import przeprowadz_ewolucje, harmonogram_do_dataframe, fitness
import os
import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def pipeline():
    '''Wczytywanie danych wejściowych'''
    data_path = ROOT / "data" / "input"
    data_folder = 'data/input'
    umiejetnosci = wczytaj_umiejetnosci(os.path.join( data_path, "znajomosc_zajec.xlsx"))
    rozklad_zajec_miesiac = wczytaj_rozklad_zajec(os.path.join( data_path, "zajęcia.xlsx"))
    dyspozycyjnosc = wczytaj_dyspozycyjnosc(os.path.join( data_path, "grafik.xlsx"))
    kalendarz = wczytaj_kalendarz(os.path.join( data_path, "grafik.xlsx"))
    rozklad_miesiac = wczytaj_rozklad_zajec_miesiac(os.path.join( data_path, "zajęcia.xlsx"), os.path.join( data_path, "grafik.xlsx"))
    print("Wgrano pliki wejsciowe")
    '''Walidacja poprawności wgranych plików'''
    print('Waliduję przesłane pliki...')
    i = 0
    if len(waliduj_df(umiejetnosci)) < 1:
        print("Plik z umiejętnościami wgrany poprawnie")
        i = i+1
    else:
        print("Plik umiejętności zawiera błędy")
    if len(waliduj_df(rozklad_zajec_miesiac)) < 1:
        print("Plik z rozkładem zajęć wgrany poprawnie")
        i = i+1
    else:
        print("Plik rozkład zajęć zawiera błędy")
        print(waliduj_df(rozklad_zajec_miesiac))

    if len(waliduj_df(dyspozycyjnosc)) < 1:
        print("Plik z dyspozycyjnością wgrany poprawnie")
        i = i+1
    else:
        print("Plik dyspozycyjność zawiera błędy")
    #sprawdz_kolumny_i_typy(rozklad_miesiac)
    #sprawdz_kolumny_i_typy(kalendarz)
    if i == 3:
        print("Wszystkie wgrane pliki są poprawne")
    else:
        print("Wgrane pliki zawierają błędy")


    # Po wywołaniu algorytmu genetycznego
    populacja, pokolenie, historia_fitness = przeprowadz_ewolucje(umiejetnosci, rozklad_miesiac, dyspozycyjnosc)


    # Pobierz najlepszy harmonogram (pierwszy w posortowanej populacji)
    najlepszy_harmonogram = populacja[0]

    # Konwertuj do DataFrame
    df_wynik = harmonogram_do_dataframe(najlepszy_harmonogram, rozklad_miesiac, dyspozycyjnosc)
    id_pracownikow = dyspozycyjnosc['pracownik'].unique()
    # Wyświetl
    print(df_wynik)

    # Opcjonalnie zapisz do CSV
    results_dir = ROOT / "data" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    df_wynik.to_csv(results_dir / "harmonogram.csv", index=False)

    # Wyświetl statystyki
    print(f"\nOsiągnięte fitness: {fitness(najlepszy_harmonogram, id_pracownikow)}")
    print(f"Liczba pokoleń: {pokolenie}")

if __name__ == "__main__":
    pipeline()
