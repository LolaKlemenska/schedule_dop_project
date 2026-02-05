import unittest
from datetime import time
from src.generowanie_harmonogramu import *

random.seed(42)


class TestPrzygotujDane(unittest.TestCase):
    def setUp(self):
        self.df_umiejetnosci = pd.DataFrame({
            'pracownik': ['Ala', 'Ola', 'Ala'],
            'nazwa_zajec': ['Matematyka', 'Fizyka', 'Fizyka'],
            'rola': ['prowadzący', 'asystent', 'prowadzący'],
            'udział': [1, 0, 1]
        })

        self.df_rozklad_zajec_miesiac = pd.DataFrame({
            'dzien_miesiaca': [1, 2],
            'dzien_tygodnia': ['poniedziałek', 'wtorek'],
            'czas': ['08:00-09:30', '10:00-11:30'],
            'sala': ['101', '202'],
            'nazwa_zajec': ['Matematyka', 'Fizyka']
        })

        self.df_dyspozycyjnosc = pd.DataFrame({
            'pracownik': ['Ala', 'Ola'],
            'dzień_miesiąca': [1, 2],
            'godziny': ['08:00-12:00', '10:00-14:00']
        })

    def test_umiejetnosci_filtruje_udzial(self):
        umiejetnosci, _, _, _ = przygotuj_dane(
            self.df_umiejetnosci,
            self.df_rozklad_zajec_miesiac,
            self.df_dyspozycyjnosc
        )
        self.assertEqual(umiejetnosci, {
            ('Ala', 'Matematyka', 'prowadzący'),
            ('Ala', 'Fizyka', 'prowadzący')
        })

    def test_zajecia_maja_poprawna_strukture(self):
        _, zajecia, _, _ = przygotuj_dane(
            self.df_umiejetnosci,
            self.df_rozklad_zajec_miesiac,
            self.df_dyspozycyjnosc
        )
        self.assertIsInstance(zajecia, list)
        self.assertEqual(len(zajecia), 2)
        self.assertSetEqual(set(zajecia[0].keys()), {
            'id', 'dzien_miesiaca', 'dzien_tygodnia', 'czas', 'sala', 'nazwa_zajec'
        })

    def test_dyspozycyjnosc_jako_set(self):
        _, _, dyspozycyjnosc, _ = przygotuj_dane(
            self.df_umiejetnosci,
            self.df_rozklad_zajec_miesiac,
            self.df_dyspozycyjnosc
        )
        self.assertEqual(dyspozycyjnosc, {
            ('Ala', 1, '08:00-12:00'),
            ('Ola', 2, '10:00-14:00')
        })

    def test_id_pracownikow_unikalne(self):
        _, _, _, id_pracownikow = przygotuj_dane(
            self.df_umiejetnosci,
            self.df_rozklad_zajec_miesiac,
            self.df_dyspozycyjnosc
        )
        self.assertSetEqual(set(id_pracownikow), {'Ala', 'Ola'})


class TestGenerujListeDostepnychPrac(unittest.TestCase):
    def test_pelna_dostepnosc_10(self):
        dyspozycyjnosc = {(1, 5, '10'), (2, 5, '5_1')}
        pracownicy = [1, 2]
        wynik = generuj_liste_dostepnych_prac(
            dzien=5, godzina=datetime.time(14, 0),
            dyspozycyjnosc=dyspozycyjnosc, pracownicy=pracownicy
        )
        self.assertEqual(wynik, [1])

    def test_pierwsza_polowa_dnia_5_1(self):
        dyspozycyjnosc = {(1, 5, '5_1'), (2, 5, '5_2')}
        pracownicy = [1, 2]
        wynik = generuj_liste_dostepnych_prac(
            dzien=5, godzina=datetime.time(9, 30),
            dyspozycyjnosc=dyspozycyjnosc, pracownicy=pracownicy
        )
        self.assertEqual(wynik, [1])

    def test_druga_polowa_dnia_5_2(self):
        dyspozycyjnosc = {(1, 5, '5_2'), (2, 5, '5_1')}
        pracownicy = [1, 2]
        wynik = generuj_liste_dostepnych_prac(
            dzien=5, godzina=datetime.time(14, 30),
            dyspozycyjnosc=dyspozycyjnosc, pracownicy=pracownicy
        )
        self.assertEqual(wynik, [1])

    def test_nikt_niedostepny_poza_godzinami(self):
        dyspozycyjnosc = {(1, 5, '5_1'), (2, 5, '5_2')}
        pracownicy = [1, 2]
        wynik = generuj_liste_dostepnych_prac(
            dzien=5, godzina=datetime.time(12, 0),
            dyspozycyjnosc=dyspozycyjnosc, pracownicy=pracownicy
        )
        self.assertEqual(wynik, [])

    def test_pracownicy_jako_stringi(self):
        dyspozycyjnosc = {(1, 5, '10')}
        pracownicy = ['1']
        wynik = generuj_liste_dostepnych_prac(
            dzien=5, godzina=datetime.time(10, 0),
            dyspozycyjnosc=dyspozycyjnosc, pracownicy=pracownicy
        )
        self.assertEqual(wynik, [1])


class TestGenerujListeKompetentnychPracownikow(unittest.TestCase):
    def test_wszystkie_pasujace(self):
        pracownicy = [1, 2, 3]
        umiejetnosci = {(1, 'Matematyka', 'prowadzący'),
                        (2, 'Matematyka', 'prowadzący'),
                        (3, 'Matematyka', 'prowadzący')}
        wynik = generuj_liste_kompetentnych_pracowników(
            pracownicy, 'Matematyka', 'prowadzący', umiejetnosci
        )
        self.assertEqual(wynik, [1, 2, 3])

    def test_czesc_pasujaca(self):
        pracownicy = [1, 2, 3]
        umiejetnosci = {(1, 'Matematyka', 'prowadzący'), (3, 'Matematyka', 'prowadzący')}
        wynik = generuj_liste_kompetentnych_pracowników(
            pracownicy, 'Matematyka', 'prowadzący', umiejetnosci
        )
        self.assertEqual(wynik, [1, 3])

    def test_brak_pasujacych(self):
        pracownicy = [1, 2]
        umiejetnosci = {(3, 'Matematyka', 'prowadzący')}
        wynik = generuj_liste_kompetentnych_pracowników(
            pracownicy, 'Matematyka', 'prowadzący', umiejetnosci
        )
        self.assertEqual(wynik, [])

    def test_inna_rola(self):
        pracownicy = [1, 2]
        umiejetnosci = {(1, 'Matematyka', 'asystent'), (2, 'Matematyka', 'prowadzący')}
        wynik = generuj_liste_kompetentnych_pracowników(
            pracownicy, 'Matematyka', 'prowadzący', umiejetnosci
        )
        self.assertEqual(wynik, [2])

    def test_inna_nazwa_zajec(self):
        pracownicy = [1, 2]
        umiejetnosci = {(1, 'Fizyka', 'prowadzący'), (2, 'Matematyka', 'prowadzący')}
        wynik = generuj_liste_kompetentnych_pracowników(
            pracownicy, 'Matematyka', 'prowadzący', umiejetnosci
        )
        self.assertEqual(wynik, [2])

class TestGenerujOsobnika(unittest.TestCase):
    def setUp(self):
        self.umiejetnosci = {
            (1, 'Matematyka', 'prowadzenie'),
            (2, 'Matematyka', 'asysta'),
            (3, 'Fizyka', 'prowadzenie'),
        }
        self.rozklad_zajec_miesiac = [
            {'dzien_miesiaca': 1, 'czas': '08:00-09:30', 'nazwa_zajec': 'Matematyka'},
            {'dzien_miesiaca': 2, 'czas': '10:00-11:30', 'nazwa_zajec': 'Fizyka'},
        ]
        self.dyspozycyjnosc = {
            (1, 1, '10'), (2, 1, '10'), (3, 2, '10')
        }
        self.id_pracownikow = [1, 2, 3]

    def test_generuj_osobnika_podstawowy(self):
        osobnik = generuj_osobnika(
            self.umiejetnosci,
            self.rozklad_zajec_miesiac,
            self.dyspozycyjnosc,
            self.id_pracownikow
        )
        self.assertEqual(len(osobnik), len(self.rozklad_zajec_miesiac))
        for prow, asys in osobnik:
            self.assertIn(prow, self.id_pracownikow + [-1])
            self.assertIn(asys, self.id_pracownikow + [-1])
            if prow != -1 and asys != -1:
                self.assertNotEqual(prow, asys)

    def test_generuj_osobnika_brak_dostepnych(self):
        dysp = set()
        osobnik = generuj_osobnika(
            self.umiejetnosci,
            [{'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'}],
            dysp,
            [1,2]
        )
        self.assertEqual(osobnik, [(-1, -1)])


class TestGenerujPopulacje(unittest.TestCase):
    def setUp(self):
        self.umiejetnosci = {(1, 'Matematyka', 'prowadzenie'), (2, 'Matematyka', 'asysta')}
        self.rozklad = [
            {'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'},
            {'dzien_miesiaca':2,'czas':'10:00-11:30','nazwa_zajec':'Matematyka'}
        ]
        self.dyspozycyjnosc = {(1,1,'10'), (2,1,'10'), (1,2,'10'), (2,2,'10')}
        self.id_pracownikow = [1,2]

    def test_generuj_populacje_dlugosc(self):
        populacja = generuj_populacje(
            5, self.umiejetnosci, self.rozklad, self.dyspozycyjnosc, self.id_pracownikow
        )
        self.assertEqual(len(populacja), 5)
        for osobnik in populacja:
            self.assertEqual(len(osobnik), len(self.rozklad))
            for prow, asys in osobnik:
                self.assertIsInstance(prow, int)
                self.assertIsInstance(asys, int)

    def test_generuj_populacje_brak_dostepnych(self):
        populacja = generuj_populacje(
            3, {(1,'Matematyka','prowadzenie')},
            [{'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'}],
            set(),
            [1]
        )
        for osobnik in populacja:
            self.assertEqual(osobnik, [(-1,-1)])


class TestPoliczObciazeniePracownikow(unittest.TestCase):
    def test_typowy(self):
        id_prac = [1,2,3]
        harmonogram = [(1,2),(2,3),(-1,1)]
        wynik = policz_obciazenie_pracownikow(id_prac, harmonogram)
        self.assertEqual(wynik, {1:2, 2:2, 3:1})

    def test_brak_przypisanego(self):
        id_prac = [1,2]
        harmonogram = [(-1,-1),(-1,-1)]
        wynik = policz_obciazenie_pracownikow(id_prac, harmonogram)
        self.assertEqual(wynik, {1:0,2:0})

    def test_czescowo_przypisane(self):
        id_prac = [1,2,3]
        harmonogram = [(1,-1),(-1,2),(3,1)]
        wynik = policz_obciazenie_pracownikow(id_prac, harmonogram)
        self.assertEqual(wynik, {1:2,2:1,3:1})


class TestFitness(unittest.TestCase):
    def test_prosty_przyklad(self):
        id_prac = [1,2,3]
        osobnik = [(1,2),(2,3),(-1,1)]
        wynik = fitness(osobnik, id_prac)
        obciazenie = {1:2,2:2,3:1}
        sred = sum(obciazenie.values())/len(obciazenie)
        kara = sum(abs(v-sred) for v in obciazenie.values())
        nagroda = 0
        oczekiwany = -kara + nagroda
        self.assertAlmostEqual(wynik, oczekiwany)

    def test_z_zleceniowcami(self):
        id_prac = [16,17,5]
        osobnik = [(16,17),(17,16),(5,-1)]
        wynik = fitness(osobnik,id_prac)
        obciazenie={16:2,17:2,5:1}
        sred=sum(obciazenie.values())/len(obciazenie)
        kara=sum(abs(v-sred) for v in obciazenie.values())
        nagroda=obciazenie[16]+obciazenie[17]
        oczekiwany=-kara+3*nagroda
        self.assertAlmostEqual(wynik, oczekiwany)


class TestSelekcjaPary(unittest.TestCase):
    def test_rozmiar(self):
        populacja=[[(1,-1),(2,-1)],[(2,-1),(1,-1)],[(1,2),(2,1)]]
        id_prac=[1,2]
        para=selekcja_pary(populacja,id_prac)
        self.assertEqual(len(para),2)
        for osobnik in para:
            self.assertIn(osobnik,populacja)

    def test_nie_ujemne_wagi(self):
        populacja=[[(1,-1)],[(2,-1)],[(-1,-1)]]
        id_prac=[1,2]
        try:
            para=selekcja_pary(populacja,id_prac)
        except ValueError:
            self.fail("selekcja_pary rzuciła ValueError przy ujemnych wagach")


class TestCrossover(unittest.TestCase):
    def test_dlugosc_wyniku(self):
        o1=[(1,2),(3,4),(5,6)]
        o2=[(6,5),(4,3),(2,1)]
        nowy1, nowy2 = crossover(o1,o2)
        self.assertEqual(len(nowy1),len(o1))
        self.assertEqual(len(nowy2),len(o2))
        for e in nowy1+nowy2:
            self.assertIsInstance(e,tuple)

    def test_point_within_bounds(self):
        random.seed(1)
        o1=[(1,1),(2,2),(3,3),(4,4)]
        o2=[(5,5),(6,6),(7,7),(8,8)]
        nowy1, nowy2=crossover(o1,o2)
        self.assertEqual(set(o1+o2), set(nowy1+nowy2))

    def test_krotkie_osobniki(self):
        o1=[(1,2)]
        o2=[(3,4)]
        nowy1, nowy2=crossover(o1,o2)
        self.assertEqual(nowy1,o1)
        self.assertEqual(nowy2,o2)

    def test_roznica_dlugosci(self):
        o1=[(1,2),(3,4)]
        o2=[(5,6)]
        with self.assertRaises(ValueError):
            crossover(o1,o2)


class TestMutacja(unittest.TestCase):
    def setUp(self):
        self.osobnik=[(1,2),(3,4)]
        self.umiejetnosci={(1,'Matematyka','prowadzenie'),(2,'Matematyka','asysta'),
                           (3,'Fizyka','prowadzenie'),(4,'Fizyka','asysta')}
        self.rozklad=[{'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'},
                      {'dzien_miesiaca':2,'czas':'10:00-11:30','nazwa_zajec':'Fizyka'}]
        self.dyspozycyjnosc={(1,1,'10'),(2,1,'10'),(3,2,'10'),(4,2,'10')}
        self.id_prac=[1,2,3,4]

    def test_zachowuje_dl(self):
        nowy=mutacja(copy.deepcopy(self.osobnik),self.umiejetnosci,self.rozklad,
                     self.dyspozycyjnosc,self.id_prac,liczba_mutacji=1)
        self.assertEqual(len(nowy),len(self.osobnik))
        for e in nowy:
            self.assertIsInstance(e,tuple)
            self.assertEqual(len(e),2)

    def test_zachowuje_kompetencje(self):
        osob=[(1,2)]
        nowy=mutacja(copy.deepcopy(osob), {(1,'Matematyka','prowadzenie'),(2,'Matematyka','asysta')},
                     [{'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'}],
                     {(1,1,'10'),(2,1,'10')}, [1,2], liczba_mutacji=5)
        for (prow, asys), zaj in zip(nowy,[{'nazwa_zajec':'Matematyka'}]):
            if prow!=-1:
                self.assertIn((prow,zaj['nazwa_zajec'],'prowadzenie'),{(1,'Matematyka','prowadzenie')})
            if asys!=-1:
                self.assertIn((asys,zaj['nazwa_zajec'],'asysta'),{(2,'Matematyka','asysta')})

    def test_prawdopodobienstwo_zero(self):
        osob=[(1,2)]
        nowy=mutacja(copy.deepcopy(osob), {(1,'Matematyka','prowadzenie'),(2,'Matematyka','asysta')},
                     [{'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'}],
                     {(1,1,'10'),(2,1,'10')}, [1,2], liczba_mutacji=5, prawdopodobienstwo=0)
        self.assertEqual(nowy,osob)


class TestSprawdzZajetosci(unittest.TestCase):
    def test_typowy(self):
        osobnik=[(1,2),(2,-1),(-1,3)]
        rozklad=[{'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'},
                 {'dzien_miesiaca':2,'czas':'10:00-11:30','nazwa_zajec':'Fizyka'},
                 {'dzien_miesiaca':3,'czas':'12:00-13:30','nazwa_zajec':'Chemia'}]
        wynik=sprawdz_zajetosci(osobnik,rozklad)
        self.assertEqual(dict(wynik), {(1,'08:00-09:30'):{1,2}, (2,'10:00-11:30'):{2}, (3,'12:00-13:30'):{3}})

    def test_ignoruj_minus1(self):
        osobnik=[(-1,-1)]
        rozklad=[{'dzien_miesiaca':1,'czas':'08:00-09:30','nazwa_zajec':'Matematyka'}]
        wynik=sprawdz_zajetosci(osobnik,rozklad)
        self.assertEqual(dict(wynik), {(1,'08:00-09:30'):set()})

    def test_pusty_osobnik(self):
        wynik=sprawdz_zajetosci([],[])
        self.assertEqual(dict(wynik),{})


class TestPrzeprowadzEwolucje(unittest.TestCase):
    def test_basic(self):
        df_umiejetnosci = pd.DataFrame({
            'pracownik': [1,2,3,4],
            'nazwa_zajec': ['Matematyka','Matematyka','Fizyka','Fizyka'],
            'rola': ['prowadzenie','asysta','prowadzenie','asysta'],
            'udział': [1,1,1,1]
        })
        df_rozklad = pd.DataFrame({
            'dzien_miesiaca':[1,2],
            'dzien_tygodnia':[1,2],
            'czas':['08:00-09:30','10:00-11:30'],
            'sala':['A','B'],
            'nazwa_zajec':['Matematyka','Fizyka']
        })
        df_dysp = pd.DataFrame({
            'pracownik':[1,2,3,4],
            'dzień_miesiąca':[1,1,2,2],
            'godziny':['10','10','10','10']
        })

        populacja, liczba_gen, historia = przeprowadz_ewolucje(
            df_umiejetnosci, df_rozklad, df_dysp,
            fitness_limit=10, limit_generacji=5, rozmiar_populacji=4
        )

        self.assertEqual(len(populacja),4)
        for o in populacja:
            for el in o:
                self.assertIsInstance(el,tuple)
                self.assertEqual(len(el),2)
        self.assertLessEqual(liczba_gen,5)
        self.assertGreaterEqual(len(historia),1)
        for f in historia:
            self.assertIsInstance(f,(int,float))

class TestHarmonogramDoDataFrame(unittest.TestCase):

    def setUp(self):
        # przykładowy df rozkładu zajęć
        self.df_rozklad = pd.DataFrame({
            'dzien_miesiaca': [2, 1],
            'dzien_tygodnia': ['Pon', 'Wt'],
            'czas': [time(9, 0), time(8, 0)],
            'sala': ['A1', 'B2'],
            'nazwa_zajec': ['Matematyka', 'Fizyka']
        })
        # df umiejętności (nieużywany w funkcji, ale wymagany jako argument)
        self.df_umiejetnosci = pd.DataFrame({
            'pracownik': [1, 2, 3],
            'specjalizacja': ['math', 'phys', 'chem'],
            'nazwa_zajec': ['Matematyka', 'Fizyka', 'Chemia'],
            'rola': ['P', 'P', 'P'],
            'udział': [1, 1, 1]
        })

    def test_poprawne_przypisanie_pracownikow(self):
        najlepszy_osobnik = [(1, 2), (3, -1)]
        df_harmonogram = harmonogram_do_dataframe(
            najlepszy_osobnik,
            self.df_rozklad,
            self.df_umiejetnosci
        )

        # sprawdzenie kolumn
        self.assertListEqual(
            list(df_harmonogram.columns),
            ['dzień_miesiąca', 'dzień_tygodnia', 'godzina', 'sala', 'nazwa_zajęć', 'prowadzący_ID', 'asystent_ID']
        )

        # wiersz dla dnia 1
        dzien_1 = df_harmonogram[df_harmonogram['dzień_miesiąca'] == 1].iloc[0]
        self.assertEqual(dzien_1['prowadzący_ID'], 'pracownik 3')
        self.assertEqual(dzien_1['asystent_ID'], 'BRAK')

        # wiersz dla dnia 2
        dzien_2 = df_harmonogram[df_harmonogram['dzień_miesiąca'] == 2].iloc[0]
        self.assertEqual(dzien_2['prowadzący_ID'], 'pracownik 1')
        self.assertEqual(dzien_2['asystent_ID'], 'pracownik 2')

    def test_sortowanie_po_dniu_i_godzinie(self):
        najlepszy_osobnik = [(1, 2), (3, -1)]
        df_harmonogram = harmonogram_do_dataframe(
            najlepszy_osobnik,
            self.df_rozklad,
            self.df_umiejetnosci
        )

        # sprawdzamy, że dni i godziny są posortowane
        dni = df_harmonogram['dzień_miesiąca'].tolist()
        godziny = df_harmonogram['godzina'].tolist()

        self.assertEqual(dni, sorted(dni))
        self.assertEqual(godziny, [time(8, 0), time(9, 0)])

    def test_BRAK_przy_wszystkich_minus_jeden(self):
        najlepszy_osobnik = [(-1, -1), (-1, -1)]
        df_harmonogram = harmonogram_do_dataframe(
            najlepszy_osobnik,
            self.df_rozklad,
            self.df_umiejetnosci
        )

        self.assertTrue((df_harmonogram['prowadzący_ID'] == 'BRAK').all())
        self.assertTrue((df_harmonogram['asystent_ID'] == 'BRAK').all())

if __name__ == '__main__':
    unittest.main(verbosity=2)


