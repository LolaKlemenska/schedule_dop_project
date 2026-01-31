import pandas as pd
from src.walidacja_danych import *

class TestWalidacjaDanych:
    def test_sprawdz_kolumny(self):
        df = pd.DataFrame(columns=['pracownik', 'specjalizacja', 'nazwa_zajec', 'rola', 'udział'])
        assert sprawdz_kolumny(df)

    def test_sprawdz_kolumny2(self):
        df = pd.DataFrame(columns=['dzien', 'czas', 'sala', 'nazwa_zajec'])
        assert sprawdz_kolumny(df)

    def test_sprawdz_kolumny3(self):
        # sprawdza czy sprawdz_kolumny zwraca True, gdy wartości kolumn są poprawne
        columns = [('dzień miesiąca', 'dzień tygodnia'),
     (1, 'cz'),
     (2, 'pt'),
     (3, 'sb'),
     (4, 'nd'),
     (5, 'pn'),
     (6, 'wt'),
     (7, 'śr'),
     (8, 'cz'),
     (9, 'pt'),
     (10, 'sb'),
     (11, 'nd'),
     (12, 'pn'),
     (13, 'wt'),
     (14, 'śr'),
     (15, 'cz'),
     (16, 'pt'),
     (17, 'sb'),
     (18, 'nd'),
     (19, 'pn'),
     (20, 'wt'),
     (21, 'śr'),
     (22, 'cz'),
     (23, 'pt'),
     (24, 'sb'),
     (25, 'nd'),
     (26, 'pn'),
     (27, 'wt'),
     (28, 'śr'),
     (29, 'cz'),
     (30, 'pt'),
     (31, 'sb')]
        df = pd.DataFrame(columns=columns)

        assert sprawdz_kolumny(df)

    def test_sprawdz_kolumny4(self):
        # Sprawdza czy sprawdz_kolumny zwraca False, gdy jest za mało dni miesiąca
        columns = [('dzień miesiąca', 'dzień tygodnia'),
                   (1, 'cz'),
                   (2, 'pt'),
                   (3, 'sb'),
                   (4, 'nd'),
                   (5, 'pn'),
                   (6, 'wt'),
                   (7, 'śr'),
                   (8, 'cz'),
                   (9, 'pt'),
                   (10, 'sb'),
                   (11, 'nd'),
                   (12, 'pn'),
                   (13, 'wt'),
                   (14, 'śr'),
                   (15, 'cz'),
                   (16, 'pt'),
                   (17, 'sb'),
                   (18, 'nd'),
                   (19, 'pn')]
        df = pd.DataFrame(columns=columns)
        assert not sprawdz_kolumny(df)

    def test_sprawdz_kolumny5(self):
        #sprawdza czy sprawdz_kolumny zawraca False, gdy jedna z wartości dni miesiąca jest większa niż 31
        columns = [('dzień miesiąca', 'dzień tygodnia'),
                   (1, 'cz'),
                   (2, 'pt'),
                   (3, 'sb'),
                   (4, 'nd'),
                   (5, 'pn'),
                   (6, 'wt'),
                   (7, 'śr'),
                   (8, 'cz'),
                   (9, 'pt'),
                   (10, 'sb'),
                   (11, 'nd'),
                   (12, 'pn'),
                   (13, 'wt'),
                   (14, 'śr'),
                   (15, 'cz'),
                   (16, 'pt'),
                   (17, 'sb'),
                   (18, 'nd'),
                   (19, 'pn'),
                   (2000, 'wt'),
                   (21, 'śr'),
                   (22, 'cz'),
                   (23, 'pt'),
                   (24, 'sb'),
                   (25, 'nd'),
                   (26, 'pn'),
                   (27, 'wt'),
                   (28, 'śr'),
                   (29, 'cz'),
                   (30, 'pt'),
                   (31, 'sb')]

        df = pd.DataFrame(columns=columns)
        assert not sprawdz_kolumny(df)

    def test_sprawdz_kolumny6(self):
        # sprawdza czy sprawdz_kolumny zawraca True, gdy miesiąc jest najkrótszy w roku
        columns = [('dzień miesiąca', 'dzień tygodnia'),
                   (1, 'cz'),
                   (2, 'pt'),
                   (3, 'sb'),
                   (4, 'nd'),
                   (5, 'pn'),
                   (6, 'wt'),
                   (7, 'śr'),
                   (8, 'cz'),
                   (9, 'pt'),
                   (10, 'sb'),
                   (11, 'nd'),
                   (12, 'pn'),
                   (13, 'wt'),
                   (14, 'śr'),
                   (15, 'cz'),
                   (16, 'pt'),
                   (17, 'sb'),
                   (18, 'nd'),
                   (19, 'pn'),
                   (20, 'wt'),
                   (21, 'śr'),
                   (22, 'cz'),
                   (23, 'pt'),
                   (24, 'sb'),
                   (25, 'nd'),
                   (26, 'pn'),
                   (27, 'wt'),
                   (28, 'śr')]

        df = pd.DataFrame(columns=columns)
        assert sprawdz_kolumny(df)

    def test_sprawdz_kolumny7(self):
        # sprawdza czy sprawdz_kolumny zawraca False, gdy dni tygodnia nie są w dobrej kolejności
        columns = [('dzień miesiąca', 'dzień tygodnia'),
                   (1, 'cz'),
                   (2, 'pt'),
                   (3, 'pn'),
                   (4, 'nd'),
                   (5, 'pn'),
                   (6, 'wt'),
                   (7, 'wt'),
                   (8, 'cz'),
                   (9, 'pt'),
                   (10, 'sb'),
                   (11, 'nd'),
                   (12, 'pn'),
                   (13, 'wt'),
                   (14, 'śr'),
                   (15, 'cz'),
                   (16, 'pt'),
                   (17, 'wt'),
                   (18, 'nd'),
                   (19, 'pn'),
                   (20, 'wt'),
                   (21, 'śr'),
                   (22, 'nd'),
                   (23, 'pt'),
                   (24, 'sb'),
                   (25, 'nd'),
                   (26, 'pn'),
                   (27, 'wt'),
                   (29, 'śr')]

        df = pd.DataFrame(columns=columns)
        assert not sprawdz_kolumny(df)

    def test_sprawdz_kolumny8(self):
        # sprawdza czy sprawdz_kolumny zawraca False, gdy dni miesiąca nie sa w dobrej kolejności
        columns = [('dzień miesiąca', 'dzień tygodnia'),
                   (1, 'cz'),
                   (2, 'pt'),
                   (3, 'sb'),
                   (4, 'nd'),
                   (5, 'pn'),
                   (6, 'wt'),
                   (8, 'śr'),
                   (7, 'cz'),
                   (9, 'pt'),
                   (10, 'sb'),
                   (11, 'nd'),
                   (12, 'pn'),
                   (13, 'wt'),
                   (15, 'śr'),
                   (14, 'cz'),
                   (16, 'pt'),
                   (17, 'sb'),
                   (18, 'nd'),
                   (20, 'pn'),
                   (19, 'wt'),
                   (21, 'śr'),
                   (22, 'cz'),
                   (23, 'pt'),
                   (24, 'sb'),
                   (25, 'nd'),
                   (26, 'pn'),
                   (27, 'wt'),
                   (28, 'śr'),
                   (29, 'cz'),
                   (30, 'pt')]

        df = pd.DataFrame(columns=columns)
        assert not sprawdz_kolumny(df)




