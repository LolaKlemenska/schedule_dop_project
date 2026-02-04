## lista zadań

- dokumentacja ze szczegółowym opisem co projekt robi, jakie ma mieć funckje, jakie założenie, co ma być wynikiem działania projektu
- na podstawie dokumentacji rozpisać testy czy np. funkcja x zwraca y itd.
- zaprogramowanie funkcji $x_1, x_2, \dots, x_n$, które będą zwracały wcześniej założony wynik (y) (można pracować nad kilkoma funkcjami jednocześnie - teoretycznie)
- po powyższych napisanie raportu (podsumowania) z wykonanej pracy

## Dokumentacja


### Opis projektu

**Cel projektu:**
Program służy do automatycznego generowania optymalnych harmonogramów pracy dla pracowników prowadzących zajęcia. System bierze pod uwagę umiejętności pracowników, rozkład zajęć oraz ich dyspozycyjność czasową, tworząc trzy warianty harmonogramu z podziałem na prowadzących zajęcia i asystentów.

**Wymagania i informacje:**
1. Na każde zajęcia idą dwie osoby - prowadząca i asystująca.
2. Każde zajęcia kończą się przed kolejnymi na tej samej sali, więc osoba z poprzednich zajęć może pójść na kolejne.
3. Pracownicy 1-15 są pracownikami etatowymi, a Pracownicy 16-32 to zleceniowcy.
4. W grafiku 5_1 oznacza pierwszą połowę dnia (8:15-13:15), a 5_2 drugą połowę dnia (13:15-18:15).

**Dane wejściowe:**
1. **znajomosc_zajec.xlsx** - plik zawierający umiejętności pracowników
2. **zajęcia.xlsx** - plan zajęć na dany tydzień z informacjami o godzinach zajęć i miejscu się ich odbywania
3. **grafik** - dostępność pracowników w danym okresie czasu

**Dane wyjściowe:**
Program generuje plik Excel zawierający trzy wersje optymalnego harmonogramu pracy z przypisaniem:
- Kto prowadzi dane zajęcia
- Kto asystuje przy zajęciach

**Zakładany model uczenia maszynowego**:
Metoda optymalizacji globalnej - algorytm genetyczny.

**Funkcje wymagane do działania programu:**

1. `wczytaj_umiejetnosci(sciezka_pliku)` - wczytuje dane o umiejętnościach pracowników z pliku Excel
2. `wczytaj_rozklad_zajec(sciezka_pliku)` - wczytuje rozkład zajęć na dany tydzień
3. `wczytaj_dyspozycyjnosc(sciezka_pliku)` - wczytuje informacje o dyspozycyjności pracowników
4. `walidacja_wczytanych_danych(nazwa_pliku)` - sprawdza czy w wgranym datasecie nie ma NaN, odpowiedi format, nazwy kolumn (czy się zgadzają) itd., co mogłby wprowadzić błędy na kolejnych etapach (kolejne podfunkje jak "sprawdz_NaN" itd.)
5. `generuj_harmonogram(rozklad, dyspozycyjnosc, umiejetnosci)` - generuje optymalny harmonogram przypisując pracowników do zajęć (maksymalizując wartość funkcji fitnessu)
6. `zapisz_harmonogram(harmonogram, sciezka_pliku)` - zapisuje wygenerowane harmonogramy do pliku Excel

Zakładamy zapisywanie 3 najoptymalniejszych wygenerowanych harmonogramów.


**Funkcja fitnessu (optymalizacji):**
1. Równomierne rozłożenie obciążenia między pracowników
2. Wykorzystanie Pracowników 16-32 częściej niż 1-15
3. Zwiększanie znajomości zajęć przez zespół
4. Wpisanie na prowadzenie Pracowników, którzy mogą je prowadzić (mają 1 w znajomości zajęć)

opcja XGBoost zamiast algorytmu genetycznego
