import unittest
from src.walidacja_danych import *

class TestSprawdzKolumny(unittest.TestCase):

    def test_umiejetnosci(self):
        df = pd.DataFrame(columns=['pracownik', 'specjalizacja', 'nazwa_zajec', 'rola', 'udział'])
        self.assertEqual(sprawdz_kolumny(df), 'umiejetnosci')

    def test_rozklad(self):
        df = pd.DataFrame(columns=['dzien', 'czas', 'sala', 'nazwa_zajec'])
        self.assertEqual(sprawdz_kolumny(df), 'rozklad')

    def test_dyspozycyjnosc(self):
        df = pd.DataFrame(columns=["pracownik", "dzień_miesiąca", "dzień_tygodnia", "godziny"])
        self.assertEqual(sprawdz_kolumny(df), 'dyspozycyjnosc')

    def test_rozklad_miesiac(self):
        df = pd.DataFrame(columns=["dzien_miesiaca", "dzien_tygodnia", "czas", "sala", "nazwa_zajec"])
        self.assertEqual(sprawdz_kolumny(df), 'rozklad_miesiac')

    def test_kalendarz(self):
        df = pd.DataFrame(columns=["dzien_miesiaca", "dzien_tygodnia"])
        self.assertEqual(sprawdz_kolumny(df), 'kalendarz')

    def test_brak_dopasowania(self):
        df = pd.DataFrame(columns=['a','b','c'])
        self.assertIsNone(sprawdz_kolumny(df))

    def test_kolejnosc_ma_znaczenie(self):
        df = pd.DataFrame(columns=['nazwa_zajec','czas','dzien','sala'])
        self.assertIsNone(sprawdz_kolumny(df))


class TestSprawdzNaN(unittest.TestCase):

    def test_brak_nan(self):
        df = pd.DataFrame({'a':[1,2], 'b':[3,4]})
        self.assertEqual(sprawdz_NaN(df), [])

    def test_istnieja_nan(self):
        df = pd.DataFrame({'a':[1, None], 'b':[None, 4]})
        wynik = sprawdz_NaN(df)
        self.assertIn(" Kolumna 'a' zawiera 1 wartości NaN.", wynik)
        self.assertIn(" Kolumna 'b' zawiera 1 wartości NaN.", wynik)

    def test_pusta_tabela(self):
        df = pd.DataFrame(columns=['a', 'b'])
        self.assertEqual(sprawdz_NaN(df), [])


class TestSprawdzTypyDanych(unittest.TestCase):

    def test_poprawne_typy(self):
        df = pd.DataFrame({'a':[1,2,3], 'b':['x','y','z'], 'c':[1,2,3]})
        oczekiwane = {'a': int, 'b': str, 'c': int}
        self.assertEqual(sprawdz_typy_danych(df, oczekiwane, nazwa="test"), [])

    def test_bledne_typy(self):
        df = pd.DataFrame({'a':[1,2,3], 'b':['x','y','z'], 'c':[None, 4, 5]})
        oczekiwane = {'a': int, 'b': str, 'c': int}
        wynik = sprawdz_typy_danych(df, oczekiwane, nazwa="test")
        self.assertEqual(wynik, ["[test] Kolumna 'c' nie ma typu int."])


class TestSprawdzZakresy(unittest.TestCase):

    def test_poprawny_zakres_liczbowy(self):
        df = pd.DataFrame({'udział':[0,1,1,0]})
        zakresy = {'udział': (0,1)}
        self.assertEqual(sprawdz_zakresy(df, zakresy), [])

    def test_bledny_zakres_liczbowy(self):
        df = pd.DataFrame({'udział':[0,2,1]})
        zakresy = {'udział': (0,1)}
        wynik = sprawdz_zakresy(df, zakresy)
        self.assertIn("[DataFrame] Kolumna 'udział' zawiera wartości poza zakresem [0, 1] (liczba: 1).", wynik)

    def test_poprawny_zakres_czasowy(self):
        df = pd.DataFrame({'czas':[time(8,0), time(12,0)]})
        zakresy = {'czas': (time(0,0), time(23,59))}
        self.assertEqual(sprawdz_zakresy(df, zakresy), [])

    def test_bledny_zakres_czasowy(self):
        df = pd.DataFrame({'czas':[time(8,0), time(23,59,59)]})
        zakresy = {'czas': (time(0,0), time(23,0))}
        wynik = sprawdz_zakresy(df, zakresy)
        self.assertIn("[DataFrame] Kolumna 'czas' zawiera wartości poza zakresem [00:00:00, 23:00:00] (liczba: 1).", wynik)


class TestWalidujDF(unittest.TestCase):

    def test_walidacja_poprawna(self):
        df = pd.DataFrame({
            'pracownik':[1],
            'specjalizacja':['matematyka'],
            'nazwa_zajec':['algebra'],
            'rola':['prowadzenie'],
            'udział':[1]
        })
        self.assertEqual(waliduj_df(df), [])

    def test_walidacja_z_bledami(self):
        df = pd.DataFrame({
            'pracownik':[1, None],
            'specjalizacja':['matematyka', 'fizyka'],
            'nazwa_zajec':['algebra', 'mechanika'],
            'rola':['prowadzenie', 'asysta'],
            'udział':[1, 2]
        })
        wynik = waliduj_df(df)
        self.assertIn(" Kolumna 'pracownik' zawiera 1 wartości NaN.", wynik)
        self.assertIn("[umiejetnosci] Kolumna 'udział' zawiera wartości poza zakresem [0, 1] (liczba: 1).", wynik)


if __name__ == "__main__":
    unittest.main(verbosity=2)
