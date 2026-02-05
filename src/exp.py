import datetime
import copy

from wczytywanie_danych import *
from pathlib import Path
from generowanie_harmonogramu import *

def exp():
    #print("Hello from zaliczenie-projekt!")
    data_path = Path.cwd().parents[0] / "data"
    df_rozklad_zajec = wczytaj_rozklad_zajec(str(data_path) + '/zajęcia.xlsx')
    print(df_rozklad_zajec.iloc[13:17])
    df_rozklad_zajec.dropna(subset = ['nazwa_zajec'], inplace=True)
    print(type(df_rozklad_zajec['czas'][0]))

    df_dyspozycyjnosc = wczytaj_dyspozycyjnosc(str(data_path) + '/grafik.xlsx')
    print(df_dyspozycyjnosc.head())
    #print(df_grafik['pracownik'].unique())

    df_umiejetnosci = wczytaj_umiejetnosci(str(data_path) + '/znajomosc_zajec.xlsx')
    #df_umiejetnosci = df_umiejetnosci.iloc[20:]
    print(df_umiejetnosci.head())
    print(df_umiejetnosci['rola'].unique())

    print(wczytaj_kalendarz(str(data_path) + '/grafik.xlsx'))

    df_rozklad_miesiac = wczytaj_rozklad_zajec_miesiac(str(data_path) + '/zajęcia.xlsx' ,str(data_path) + '/grafik.xlsx', )
    print(df_rozklad_miesiac.head())

    umiejetnosci, dic_rozklad_zajec_miesiac, dyspozycyjnosc, id_pracownikow = przygotuj_dane(df_umiejetnosci, df_rozklad_miesiac,
                                                                             df_dyspozycyjnosc)

    '''
    print(dyspozycyjnosc)
    osobnik = generuj_osobnika(umiejetnosci, dic_rozklad_zajec_miesiac, dyspozycyjnosc, id_pracownikow)

    print(osobnik)
    print(fitness(osobnik, id_pracownikow))

    populacja = generuj_populacje(10, umiejetnosci, dic_rozklad_zajec_miesiac, dyspozycyjnosc, id_pracownikow)
    print(len(selekcja_pary(populacja, id_pracownikow)))

    #print(sum([(mutacja(osobnik, umiejetnosci, dic_rozklad_zajec_miesiac, dyspozycyjnosc, id_pracownikow) != osobnik) for _ in range(1000)]))
'''
    populacja, generacje, fitness_historia = przeprowadz_ewolucje(
        df_umiejetnosci, df_rozklad_miesiac,df_dyspozycyjnosc,
        fitness_limit = 400,
        limit_generacji = 500,
        rozmiar_populacji = 30
    )
    print(f'Generacje: {generacje}, '
          f'spadek fitness: {fitness_historia[-1] - fitness_historia[0]}, '
          f'początkowy fitness: {fitness_historia[0]}, '
          f'końcowy fitness: {fitness_historia[-1]}, '
          f'najlepszy harmonogram {populacja[0]}')

if __name__ == "__main__":
    exp()