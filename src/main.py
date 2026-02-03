from wczytywanie_danych import wczytaj_umiejetnosci, wczytaj_rozklad_zajec, wczytaj_dyspozycyjnosc, wczytaj_kalendarz, wczytaj_rozklad_zajec_miesiac
from walidacja_danych import waliduj_df
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
    print("Hello from zaliczenie-projekt!")

if __name__ == "__main__":
    pipeline()
