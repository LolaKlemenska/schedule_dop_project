import copy
import datetime
import random
from collections import defaultdict
from random import choice
import numpy as np
import pandas as pd

Osobnik = list[tuple[int,int]]
Populacja = list[Osobnik]

def przygotuj_dane(df_umiejetnosci: pd.DataFrame, df_rozklad_zajec_miesiac: pd.DataFrame, df_dyspozycyjnosc: pd.DataFrame):
    '''
    Przerabia DataFrame'y na prostsze struktury danych.

    Zwraca:
    zajecia: lista zawierająca słowniki z kluczami id, dzien_miesiaca, dzien_tygodnia, czas, sala, nazwa_zajec
    umiejetnosci: set((pracownik, nazwa_zajęć, rola))
    dyspozycyjnosc: set((pracownik, dzień_miesiąca, godziny))
    id_pracowników: lista z id_pracowników
    '''

    #zajecia = [{id, dzien_miesiaca, dzien_tygodnia, czas, sala, nazwa_zajęć}]
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

    id_pracownikow = df_dyspozycyjnosc['pracownik'].unique()

    return umiejetnosci, zajecia, dyspozycyjnosc, list(id_pracownikow)


def generuj_liste_dostepnych_prac(dzien, godzina, dyspozycyjnosc, pracownicy):
    '''Zwraca listę pracowników dostępnych w danym dniu miesiąca'''
    #5_1 oznacza pierwszą połowę dnia (8:15-13:15), a 5_2 drugą połowę dnia (13:15-18:15).
    dostepni = []
    for id_prac in pracownicy:
        id_prac = int(id_prac)
        if (id_prac, dzien, '10') in dyspozycyjnosc:
            dostepni.append(id_prac)
        elif (id_prac, dzien, '5_1') in dyspozycyjnosc:
            if datetime.time(8,0) <= godzina <= datetime.time(11,0):
                dostepni.append(id_prac)
        elif (id_prac, dzien, '5_2') in dyspozycyjnosc:
            if datetime.time(13,0) <= godzina <= datetime.time(16,0):
                dostepni.append(id_prac)
    return dostepni

def generuj_liste_kompetentnych_pracowników(pracownicy, nazwa_zajec, rola, umiejetnosci):
    kompetentni = []
    for id_prac in pracownicy:
        if (id_prac, nazwa_zajec, rola) in umiejetnosci:
            kompetentni.append(id_prac)
    return kompetentni


def generuj_osobnika(umiejetnosci: set, rozklad_zajec_miesiac:list, dyspozycyjnosc: set, id_pracownikow: list) -> Osobnik:
    osobnik = []
    zajetosci = defaultdict(set) # (dzien, czas) -> {pracownicy}; zapamiętuje, którzy pracownicy w danym dniu o danej godzinie są zajęci

    for zajecia in rozklad_zajec_miesiac:
        slot  = (zajecia['dzien_miesiaca'], zajecia['czas'])
        dostepni = generuj_liste_dostepnych_prac(zajecia['dzien_miesiaca'], zajecia['czas'], dyspozycyjnosc, id_pracownikow)
        dostepni = [p for p in dostepni if p not in zajetosci[slot]] #dostępni sa tylko ci, którzy nie prowadza żadnych innych zajęć w tym czasie
        prow, asys = -1, -1
        if dostepni:
            kompetetni_prow = generuj_liste_kompetentnych_pracowników(dostepni, zajecia['nazwa_zajec'], 'prowadzenie',
                                                                      umiejetnosci)
            # print(f'Kompetetni prow: {kompetetni_prow}')

            if kompetetni_prow:
                prow = random.choice(kompetetni_prow)
                zajetosci[slot].add(prow)

            kompetetni_asys = generuj_liste_kompetentnych_pracowników(dostepni, zajecia['nazwa_zajec'], 'asysta',
                                                                      umiejetnosci)
            # print(f'Kompetetni asys: {kompetetni_asys}')

            if prow in kompetetni_asys:
                kompetetni_asys.remove(prow)

            if kompetetni_asys:
                asys = random.choice(kompetetni_asys)
                zajetosci[slot].add(asys)

        osobnik.append((prow, asys))
    return osobnik

def generuj_populacje(rozmiar: int, umiejetnosci: set, rozklad_zajec_miesiac:list, dyspozycyjnosc: set, id_pracownikow: list) -> Populacja:
    populacja = []
    for i in range(rozmiar):
        osobnik = generuj_osobnika(umiejetnosci, rozklad_zajec_miesiac, dyspozycyjnosc, id_pracownikow)
        populacja.append(osobnik)
    return populacja

def policz_obciazenie_pracownikow(id_pracownikow: list[int], harmonogram: Osobnik) -> dict[int, int]:
    obciazenie = {id: 0 for id in id_pracownikow}
    for p1, p2 in harmonogram:
        if p1 != -1:
            obciazenie[p1] += 1
        if p2 != -1:
            obciazenie[p2] += 1

    return obciazenie


def fitness(osobnik: Osobnik, id_pracownikow: list):

    fitness = 0

    #Równomierne obciążenie pracowników
    obciazenie_pracownikow = policz_obciazenie_pracownikow(id_pracownikow, osobnik)
    sred_obciazenie = (sum(obciazenie_pracownikow.values()) / len(id_pracownikow))
    kara_rownomierne_obciazenie = sum(abs(obciazenie_pracownikow[p] - sred_obciazenie) for p in obciazenie_pracownikow)
    fitness -= 1 * kara_rownomierne_obciazenie


    #Preferencja pracowników 16-32
    nagroda_zleceniowcy = sum(
        obciazenie_pracownikow[p]
        for p in obciazenie_pracownikow
        if 16 <= p <= 32
    )
    fitness += 3 * nagroda_zleceniowcy

    return fitness

def selekcja_pary(populacja: Populacja, id_pracownikow: list) -> list[Osobnik]:
    return random.choices(
        population=populacja,
        weights=[fitness(osobnik, id_pracownikow) for osobnik in populacja],
        k=2
    )

def crossover(osobnik1: Osobnik, osobnik2: Osobnik) -> tuple[Osobnik, Osobnik]:
    if len(osobnik1) != len(osobnik2):
        raise ValueError('Osobniki, które podlegają crossoverowi muszą być tej samej długości')
    length = len(osobnik1)
    if length <= 2:
        return osobnik1, osobnik2

    p = random.randint(1, length - 1)
    return osobnik1[0:p] + osobnik2[p:], osobnik2[0:p] + osobnik1[p:]

def sprawdz_zajetosci(osobnik: Osobnik, rozklad: list[dict]) -> dict:
    zajetosci = defaultdict(set)
    for (prow, asys), zajecia in zip(osobnik, rozklad):
        slot = (zajecia['dzien_miesiaca'], zajecia['czas'])
        if prow != -1:
            zajetosci[slot].add(prow)
        if asys != -1:
            zajetosci[slot].add(asys)
    return zajetosci


def mutacja(osobnik: Osobnik,
            umiejetnosci: set,
            rozklad_zajec_miesiac:list,
            dyspozycyjnosc: set,
            id_pracownikow: list[int],
            liczba_mutacji: int = 1,
            prawdopodobienstwo: float = 0.8) -> Osobnik:

    osobnik = copy.deepcopy(osobnik)
    zajetosci = sprawdz_zajetosci(osobnik, rozklad_zajec_miesiac)

    for _ in range(liczba_mutacji):
        idx = random.randrange(len(osobnik))
        zajecia = rozklad_zajec_miesiac[idx]
        slot = (zajecia["dzien_miesiaca"], zajecia['czas'])

        dostepni = generuj_liste_dostepnych_prac(zajecia['dzien_miesiaca'], zajecia['czas'], dyspozycyjnosc, id_pracownikow)
        dostepni = [p for p in dostepni if p not in zajetosci[slot]]  # dostępni sa tylko ci, którzy nie prowadza żadnych innych zajęć w tym czasie

        kompetetni_prow = generuj_liste_kompetentnych_pracowników(dostepni, zajecia['nazwa_zajec'], 'prowadzenie', umiejetnosci)
        kompetetni_asys = generuj_liste_kompetentnych_pracowników(dostepni, zajecia['nazwa_zajec'], 'asysta', umiejetnosci)
        stary_prow, stary_asys = osobnik[idx]

        #wylosowanie prowadzącego
        if kompetetni_prow:
            prow = random.choice(kompetetni_prow)
            kompetetni_asys = [p for p in kompetetni_asys if p != prow]
        else:
            prow = stary_prow

        #wylosowanie asystującego
        if kompetetni_asys:
            asys = random.choice(kompetetni_asys)
        else:
            asys = stary_asys

        if random.random() < prawdopodobienstwo:
            if stary_prow != -1:
                zajetosci[slot].remove(stary_prow)  # stary prowadzący jest zwalniany z danego terminu
            zajetosci[slot].add(prow) #nowy prowadzący jest zajmowany na dany termin

            if stary_asys != -1:
                zajetosci[slot].remove(stary_asys)# stary asystujący jest zwalniany z danego terminu
            zajetosci[slot].add(asys) #nowy asystujący jest zajmowany na dany termin

            osobnik[idx] = (prow, asys) # ustawiamy nowo wylosowanych pracowników

    return osobnik

def przeprowadz_ewolucje(
        df_umiejetnosci: pd.DataFrame,
        df_rozklad_zajec_miesiac: pd.DataFrame,
        df_dyspozycyjnosc: pd.DataFrame,
        fitness_limit=400,
        limit_generacji=500,
        rozmiar_populacji=30
) -> tuple[Populacja, int, list]:
    umiejetnosci, zajecia, dyspozycyjnosc, id_pracownikow = przygotuj_dane(df_umiejetnosci, df_rozklad_zajec_miesiac, df_dyspozycyjnosc)
    populacja = generuj_populacje(rozmiar_populacji, umiejetnosci, zajecia, dyspozycyjnosc, id_pracownikow)
    fitness_historia = []
    for i in range(limit_generacji):
        populacja = sorted(
            populacja,
            key=lambda osobnik: fitness(osobnik, id_pracownikow),
            reverse=True
                )
        wartosc_fitness = fitness(populacja[0], id_pracownikow)
        fitness_historia.append(wartosc_fitness)

        if wartosc_fitness > fitness_limit:
            break

        nowa_generacja = populacja[0:2]

        for j in range(int(len(populacja) / 2) - 1):
            rodzice = selekcja_pary(populacja, id_pracownikow)
            potomek_a, potomek_b = crossover(rodzice[0], rodzice[1])
            potomek_a = mutacja(potomek_a,umiejetnosci, zajecia, dyspozycyjnosc, id_pracownikow)
            potomek_b = mutacja(potomek_b, umiejetnosci, zajecia, dyspozycyjnosc, id_pracownikow)
            nowa_generacja += [potomek_a, potomek_b]

        populacja = nowa_generacja

    wartosc_fitness = fitness(populacja[0], id_pracownikow)
    fitness_historia.append(wartosc_fitness)

    populacja = sorted(
        populacja,
        key=lambda osobnik: fitness(osobnik, id_pracownikow),
        reverse=True
    )

    return populacja, i, fitness_historia


def harmonogram_do_dataframe(
    najlepszy_osobnik: Osobnik,
    df_rozklad_zajec_miesiac: pd.DataFrame,
    df_umiejetnosci: pd.DataFrame
) -> pd.DataFrame:
    '''
    Konwertuje najlepszy harmonogram (osobnik) do czytelnego DataFrame.

    Args:
        najlepszy_osobnik: lista par (prowadzący_id, asystent_id)
        df_rozklad_zajec_miesiac: DataFrame z rozkładem zajęć

    Returns:
        DataFrame z kolumnami: dzień, dzień_tygodnia, godzina, sala, nazwa_zajęć, prowadzący, asystent
    '''
    dane = []
    id_pracownikow = df_umiejetnosci['pracownik'].unique()
    for idx, (prow_id, asys_id) in enumerate(najlepszy_osobnik):
        zajecia = df_rozklad_zajec_miesiac.iloc[idx]

        dane.append({
            'dzień_miesiąca': zajecia['dzien_miesiaca'],
            'dzień_tygodnia': zajecia['dzien_tygodnia'],
            'godzina': zajecia['czas'],
            'sala': zajecia['sala'],
            'nazwa_zajęć': zajecia['nazwa_zajec'],
            'prowadzący_ID': f'pracownik {prow_id}' if prow_id != -1 else 'BRAK',
            'asystent_ID': f'pracownik {asys_id}' if asys_id != -1 else 'BRAK'
        })

    df_harmonogram = pd.DataFrame(dane)
    df_harmonogram = df_harmonogram.sort_values(['dzień_miesiąca', 'godzina'])

    return df_harmonogram
