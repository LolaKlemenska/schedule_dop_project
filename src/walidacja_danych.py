import pandas as pd


def sprawdz_kolumny(df: pd.DataFrame):
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

def sprawdz_NaN(df: pd.DataFrame, nazwa: str = "DataFrame") -> list[str]:
    """Sprawdza występowanie wartości NaN."""
    bledy = []

    nan_cols = df.columns[df.isna().any()]
    for col in nan_cols:
        liczba = df[col].isna().sum()
        bledy.append(
            f"[{nazwa}] Kolumna '{col}' zawiera {liczba} wartości NaN."
        )
    if bledy == []:
        return None
    return bledy

def sprawdz_typy_danych(
    df: pd.DataFrame,
    oczekiwane_typy: dict[str, type],
    nazwa: str = "DataFrame"
) -> list[str]:
    """
    oczekiwane_typy = {
        'kolumna': typ (np. int, float, str)
    }
    """
    bledy = []

    for kol, typ in oczekiwane_typy.items():
        if kol not in df.columns:
            bledy.append(f"[{nazwa}] Brak kolumny '{kol}'.")
            continue

        if not df[kol].map(lambda x: isinstance(x, typ) or pd.isna(x)).all():
            bledy.append(
                f"[{nazwa}] Kolumna '{kol}' nie ma typu {typ.__name__}."
            )

    return bledy

def sprawdz_kolumny_i_typy(df: pd.DataFrame) -> list[str]:
    bledy = []

    SCHEMAT_TYPY = {
    "umiejetnosci": {
        "pracownik": int,
        "specjalizacja": str,
        "nazwa_zajec": str,
        "rola": str,
        "udział": (int, float)
    },
    "rozklad": {
        "dzien": str,
        "czas": str,
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
        "czas": str,
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

