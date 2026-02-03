import datetime
import random
from collections import defaultdict
from random import choice
import numpy as np
import pandas as pd

def przygotuj_dane(df_umiejetnosci: pd.DataFrame, df_rozklad_zajec_miesiac: pd.DataFrame, df_dyspozycyjnosc: pd.DataFrame):
    '''
    Przerabia DataFrame'y na prostsze struktury danych.

    Zwraca:
    zajecia: lista zawierająca słowniki z kluczami id, dzien_miesiaca, dzien_tygodnia, czas, sala, nazwa_zajec
    umiejetnosci: set((pracownik, nazwa_zajęć, rola))
    dyspozycyjnosc: set((pracownik, dzień_miesiąca, godziny))


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

    id_pracownikow = df_dyspozycyjnosc['pracownik'].unique()

    return umiejetnosci, zajecia, dyspozycyjnosc, id_pracownikow


def generuj_liste_dostepnych_prac(dzien, godzina, dyspozycyjnosc, pracownicy):
    '''Zwraca listę pracowników dostępnych w danym dniu miesiąca'''
    #5_1 oznacza pierwszą połowę dnia (8:15-13:15), a 5_2 drugą połowę dnia (13:15-18:15).
    dostepni = []
    for id_prac in pracownicy:
        id_prac = int(id_prac)
        if (id_prac, dzien, 10) in dyspozycyjnosc:
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


def generuj_osobnika(umiejetnosci: set, rozklad_zajec_miesiac:dict, dyspozycyjnosc: set, id_pracownikow: list):
    osobnik = []
    zajetosci = defaultdict(set) # (dzien, czas) -> {pracownicy}; zapamiętuje, którzy pracownicy w danym dniu o danej godzinie są zajęci

    for zajecia in rozklad_zajec_miesiac:
        slot  = (zajecia['dzien_miesiaca'], zajecia['czas'])
        dostepni = generuj_liste_dostepnych_prac(zajecia['dzien_miesiaca'], zajecia['czas'], dyspozycyjnosc, id_pracownikow)
        dostepni = [p for p in dostepni if p not in zajetosci[slot]] #dostępni sa tylko ci, którzy nie prowadza żadnych innych zajęć w tym czasie
        #print(f'Dostepni: {dostepni}')
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

