import pandas as pd
from collections import defaultdict

def przygotuj_dane(df_umiejetnosci: pd.DataFrame, df_rozklad_zajec: pd.DataFrame, df_dyspozycyjnosc: pd.DataFrame):
    '''
    Przerabia DataFrame'y na słowniki.

    Zwraca:
    dict_rozkład_zajec: słownik gdzie kluczami są dni tygodnia.
    Pod każdym kluczem jest kolejny słownik o strukturze:
     - godzina
        - sala
        - nazwa_zajec
    dict_umiejetnosci: słownik, gdzie kluczami są numery pracowników. Pod każdym kluczem jest kolejny słownik z kluczami: 'specjalizacja', 'nazwa_zajec', 'rola', 'udział'.
    dict_dyspozycyjnosc: słownik, gdzie kluczami są dni miesiąca. Pod każdym dniem miesiąca jest słownik o nastepującej strukturze:
    - dzień_miesiąca
        - dzień tygodnia
        - 'pracownicy' (każdy dzień miesiąca zawiera słownik z kluczem 'pracownicy')
            - pracownik: godziny
    '''

    dict_rozkład_zajec = defaultdict(dict)
    for _, row in df_rozklad_zajec.iterrows():
        dict_rozkład_zajec[row['dzien_tygodnia']][row['czas']] = {
                                 'sala': row['sala'],
                                 'nazwa_zajec': row['nazwa_zajec']
        }

    dict_umiejetnosci = defaultdict(dict)
    for _, row in df_umiejetnosci.iterrows():
        dict_umiejetnosci[row['pracownik']] = {
            'specjalizacja': row['specjalizacja'],
            'nazwa_zajec': row['nazwa_zajec'],
            'rola': row['rola'],
            'udział': row['udział']
        }

    dict_dyspozycyjnosc = defaultdict(lambda: defaultdict(dict))
    for i, row in df_dyspozycyjnosc.iterrows():
        dict_dyspozycyjnosc[row['dzień_miesiąca']]['dzień_tygodnia'] = row['dzień_tygodnia']
        dict_dyspozycyjnosc[row['dzień_miesiąca']]['pracownicy'][row['pracownik']] = row['godziny']

    for k, v in dict_dyspozycyjnosc.items():
        dict_dyspozycyjnosc[k] = dict(v)

    return dict(dict_umiejetnosci), dict(dict_rozkład_zajec), dict(dict_dyspozycyjnosc)

def generuj_osobnika(umiejetnosci: pd.DataFrame, rozklad_zajec: pd.DataFrame, dyspozycyjnosc: pd.DataFrame) :
    pass