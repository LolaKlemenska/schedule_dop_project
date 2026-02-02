from wczytywanie_danych import wczytaj_umiejetnosci, wczytaj_rozklad_zajec, wczytaj_dyspozycyjnosc, wczytaj_kalendarz, wczytaj_rozklad_zajec_miesiac
from walidacja_danych import sprawdz_kolumny_i_typy
from generowanie_harmonogramu import przygotuj_dane, generuj_liste_dostepnych_prac, generuj_liste_kompetentnych_pracowników, generuj_osobnika
import os

def pipeline():
    '''Wczytywanie danych wejściowych'''
    umiejetnosci = wczytaj_umiejetnosci(os.path.join("..", "data", "znajomosc_zajec.xlsx"))
    rozklad_zajec_miesiac = wczytaj_rozklad_zajec(os.path.join("..", "data", "zajęcia.xlsx"))
    dyspozycyjnosc = wczytaj_dyspozycyjnosc(os.path.join("..", "data", "grafik.xlsx"))
    kalendarz = wczytaj_kalendarz(os.path.join("..", "data", "grafik.xlsx"))
    rozklad_miesiac = wczytaj_rozklad_zajec_miesiac(os.path.join("..", "data", "zajęcia.xlsx"), os.path.join("..", "data", "grafik.xlsx"))
    print("Wgrano pliki wejsciowe")
    print("Hello from zaliczenie-projekt!")

if __name__ == "__main__":
    pipeline()
