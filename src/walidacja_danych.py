from typing import Union
import pandas as pd
from datetime import time


def sprawdz_kolumny(df: pd.DataFrame):
    """
    Sprawdza, czy kolumny DataFrame dokładnie odpowiadają jednemu
    z predefiniowanych schematów i zwraca nazwę pasującego schematu.
    Jeśli brak dopasowania, zwraca None.
    """
    schematy = {
        "umiejetnosci": ['pracownik', 'specjalizacja', 'nazwa_zajec', 'rola', 'udział'],
        "rozklad": ['dzien', 'czas', 'sala', 'nazwa_zajec'],
        "dyspozycyjnosc": ["pracownik", "dzień_miesiąca", "dzień_tygodnia", "godziny"],
        "rozklad_miesiac": ["dzien_miesiaca", "dzien_tygodnia", "czas", "sala", "nazwa_zajec"],
        "kalendarz": ["dzien_miesiaca", "dzien_tygodnia"]
    }

    for nazwa, kolumny in schematy.items():
        if list(df.columns) == kolumny:
            return nazwa

    return None

def sprawdz_NaN(df: pd.DataFrame) -> list[str]:
    """
    Sprawdza, które kolumny DataFrame zawierają wartości NaN
    i zwraca listę komunikatów.
    """
    bledy = []

    nan_cols = df.columns[df.isna().any()]
    for col in nan_cols:
        liczba = df[col].isna().sum()
        bledy.append(
            f" Kolumna '{col}' zawiera {liczba} wartości NaN."
        )
    return bledy

def sprawdz_typy_danych(
    df: pd.DataFrame,
    oczekiwane_typy: dict[str, type],
    nazwa: str = "DataFrame"
) -> list[str]:
    """
    Sprawdza zgodność typów danych w kolumnach DataFrame
    z oczekiwanymi typami i zwraca listę komunikatów.

    oczekiwane_typy = {
        'kolumna': typ (np. int, float, str)
    }
    """
    bledy = []

    for kol, typ in oczekiwane_typy.items():
        if kol not in df.columns:
            bledy.append(f"[{nazwa}] Brak kolumny '{kol}'.")
            continue

        if not df[kol].map(lambda x: isinstance(x, typ)).all():
            bledy.append(f"[{nazwa}] Kolumna '{kol}' nie ma typu {typ.__name__}.")

    return bledy

def sprawdz_kolumny_i_typy(df: pd.DataFrame) -> list[str]:
    """
    Rozpoznaje schemat kolumn DataFrame i sprawdza,
    czy typy danych są zgodne z oczekiwanym schematem.
    Zwraca listę komunikatów.
    """
    bledy = []

    SCHEMAT_TYPY = {
    "umiejetnosci": {
        "pracownik": int,
        "specjalizacja": str,
        "nazwa_zajec": str,
        "rola": str,
        "udział": int
    },
    "rozklad": {
        "dzien": str,
        "czas": time,
        "sala": str,
        "nazwa_zajec": str
    },
    "dyspozycyjnosc": {
        "pracownik": int,
        "dzień_miesiąca": int,
        "dzień_tygodnia": str,
        "godziny": str
    },
    "rozklad_miesiac": {
        "dzien_miesiaca": int,
        "dzien_tygodnia": str,
        "czas": time,
        "sala": str,
        "nazwa_zajec": str
    },
    "kalendarz": {
        "dzien_miesiaca": int,
        "dzien_tygodnia": str
        }
    }
    schemat = sprawdz_kolumny(df)
    if schemat is None:
        bledy.append("Nieznany schemat kolumn DataFrame.")
        return bledy

    bledy += sprawdz_typy_danych(
        df,
        SCHEMAT_TYPY[schemat],
        nazwa=schemat
    )

    return bledy

def sprawdz_zakresy(
    df: pd.DataFrame,
    zakresy: dict[str, tuple[Union[int, float, time], Union[int, float, time]]],
    nazwa: str = "DataFrame"
) -> list[str]:
    """
    Sprawdza, czy wartości kolumn w DataFrame mieszczą się w określonych zakresach.

    zakresy = {
        'kolumna': (min, max)
    }
    """
    bledy = []

    for kol, (min_val, max_val) in zakresy.items():
        if kol not in df.columns:
            continue

        seria = df[kol].dropna()

        if seria.empty:
            continue

        # zakres liczbowy
        if isinstance(min_val, (int, float)):
            poza = seria[(seria < min_val) | (seria > max_val)]

        # zakres czasowy (datetime.time)
        elif isinstance(min_val, time):
            poza = seria[~seria.map(lambda x: min_val <= x <= max_val)]

        else:
            continue  # nieobsługiwany typ zakresu

        if not poza.empty:
            bledy.append(
                f"[{nazwa}] Kolumna '{kol}' zawiera wartości poza zakresem "
                f"[{min_val}, {max_val}] (liczba: {len(poza)})."
            )

    return bledy

def sprawdz_kolumny_i_zakresy(df: pd.DataFrame) -> list[str]:
    """
    Rozpoznaje schemat kolumn DataFrame i sprawdza,
    czy wartości mieszczą się w dozwolonych zakresach.
    Zwraca listę komunikatów.
    """
    bledy = []

    SCHEMAT_ZAKRESY = {
        "umiejetnosci": {
            "udział": (0, 1)
        },
        "dyspozycyjnosc": {
            "dzień_miesiąca": (1, 31),
        },
        "rozklad_miesiac": {
            "dzien_miesiaca": (1, 31),
            "czas": (time(0, 0), time(23, 59, 59))
        },
        "kalendarz": {
            "dzien_miesiaca": (1, 31)
        },
        "rozklad": {
            "czas": (time(0, 0), time(23, 59, 59))
        }
    }

    schemat = sprawdz_kolumny(df)
    if schemat is None:
        return ["Nieznany schemat kolumn DataFrame."]

    zakresy = SCHEMAT_ZAKRESY.get(schemat)
    if not zakresy:
        return bledy

    bledy += sprawdz_zakresy(
        df,
        zakresy,
        nazwa=schemat
    )

    return bledy


def waliduj_df(df: pd.DataFrame) -> list[str]:
    """
    Uruchamia pełną walidację DataFrame:
    1. Sprawdza kolumny i typy danych
    2. Sprawdza wartości NaN
    3. Sprawdza, czy wartości liczbowe mieszczą się w dozwolonych zakresach
    Zwraca listę z komunikatami.
    """
    bledy = []

    bledy += sprawdz_kolumny_i_typy(df)
    bledy += sprawdz_NaN(df)
    bledy += sprawdz_kolumny_i_zakresy(df)

    return bledy