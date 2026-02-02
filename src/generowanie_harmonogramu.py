import pandas as pd
from collections import defaultdict

def przygotuj_dane(df_umiejetnosci: pd.DataFrame, df_rozklad_zajec_miesiac: pd.DataFrame, df_dyspozycyjnosc: pd.DataFrame):
    '''
    Przerabia DataFrame'y na prostsze struktury danych.

    Zwraca:
    zajecia: lista zawierająca słowniki z kluczami id, dzien, czas, sala, nazwa_zajec
    umiejetnosci: set((pracownik, nazwa_zajęć, rola))
    dyspozycyjnosc = set((pracownik, dzień_miesiąca, godziny))


    '''

    #zajecia = [{id, dzien, czas, sala, nazwa_zajęć}]
    zajecia = []
    for i, row in df_rozklad_zajec_miesiac.iterrows():
        zajecia.append(
            {'id': i,
             'dzien_miesiaca' : row['dzien_miesiaca'],
             'dzien_tygodnia': row['dzien_tygodnia'],
             'czas': row['czas'],
             'sala' : row['sala'],
             'nazwa_zajec': row['nazwa_zajec'],}
        )


    #umiejetnosci = set(pracownik, nazwa_zajęć, rola)
    umiejetnosci = set((row['pracownik'], row['nazwa_zajec'], row['rola'])
        for _, row in df_umiejetnosci.iterrows()
        if row['udział'] == 1)


    #dyspozycyjnosc = set(pracownik, dzień_miesiąca, godziny)
    dyspozycyjnosc = set((row['pracownik'], row['dzień_miesiąca'], row['godziny'])
                         for _,row in df_dyspozycyjnosc.iterrows())

    return umiejetnosci, zajecia, dyspozycyjnosc

def generuj_osobnika(umiejetnosci: pd.DataFrame, rozklad_zajec: pd.DataFrame, dyspozycyjnosc: pd.DataFrame) :
    pass