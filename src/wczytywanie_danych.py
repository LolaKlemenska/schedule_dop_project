import pandas as pd

def wczytaj_umiejetnosci(sciezka_pliku: str) -> pd.DataFrame:
    """Wczytuje dane o umiejętnościach pracowników z pliku Excel."""
    try:
        df = pd.read_excel(sciezka_pliku, header = [0,1,2], index_col = 0).fillna(0)
    except Exception as e:
        raise IOError(f"Błąd przy wczytywaniu pliku umiejętności: {e}")
    df = df.reset_index().rename(columns={'index': 'pracownik'})
    df.columns = ['pracownik'] + [f"{i}_{j}_{k}" for i,j,k in df.columns[1:]]
    df_tidy = df.melt(id_vars='pracownik', var_name='temp', value_name='udział')
    df_tidy[['specjalizacja','nazwa_zajec','rola']] = df_tidy['temp'].str.split('_', expand=True)
    df_tidy = df_tidy.drop(columns='temp')


    df_tidy = df_tidy[['pracownik','specjalizacja','nazwa_zajec','rola','udział']]
    #walidacja_wczytanych_danych(df, typ='umiejetnosci')
    return df_tidy

def wczytaj_rozklad_zajec(sciezka_pliku: str) -> pd.DataFrame:
    """Wczytuje rozkład zajęć na dany tydzień z pliku Excel."""
    try:
        raw = pd.read_excel(sciezka_pliku)
    except Exception as e:
        raise IOError(f"Błąd przy wczytywaniu rozkładu zajęć: {e}")

    raw = raw.rename(columns={raw.columns[0]: "czas"})
    dni = ["pn", "wt", "śr", "czw", "pt"]

    raw["dzien"] = raw["czas"].where(raw["czas"].isin(dni))
    raw["dzien"] = raw["dzien"].ffill()
    raw = raw[~raw["czas"].isin(dni)]
    raw = raw.drop(index=0)
    df = raw.melt(
    id_vars=["dzien", "czas"],  # kolumny, które zostają bez zmian
    value_name="nazwa_zajec",  # jak ma się nazywać nowa kolumna z wartościami
    var_name="sala"             # jak ma się nazywać nowa kolumna z nazwami kolumn
    )
    #walidacja_wczytanych_danych(df, typ='rozklad')
    return df


def wczytaj_dyspozycyjnosc(sciezka_pliku: str) -> pd.DataFrame:
    """Wczytuje informacje o dyspozycyjności pracowników z pliku Excel i zwraca w formacie długim."""
    df = pd.read_excel(
        sciezka_pliku,
        skiprows=2,
        header=[0, 1]
    )

    df = df.iloc[:, 1:-1]
    df = df.iloc[:-1, :]
    df = df.fillna(0)

    pracownicy = df[("dzień miesiąca", "dzień tygodnia")]
    df_dni = df.iloc[:, 1:]

    pracownik_col = []
    dzien_miesiaca = []
    dzien_tygodnia = []
    godziny = []

    for i, pracownik in enumerate(pracownicy):
        for j in range(df_dni.shape[1]):
            godz = df_dni.iloc[i, j]
            if godz != 0:
                dzien = df_dni.columns[j][0]
                tydz = df_dni.columns[j][1]

                # tylko liczby dni
                if isinstance(dzien, (int, float)):
                    pracownik_col.append(pracownik.lower())
                    dzien_miesiaca.append(int(dzien))
                    dzien_tygodnia.append(tydz)
                    godziny.append(godz)

    return pd.DataFrame({
        "pracownik": pracownik_col,
        "dzień_miesiąca": dzien_miesiaca,
        "dzień_tygodnia": dzien_tygodnia,
        "godziny": godziny
    })

def wczytaj_kalendarz(sciezka_pliku: str) -> pd.DataFrame:
    """Wczytuje kalendarz danego miesiąca z pliku Excel zawierającego dyspozycyjność pracowników"""
    df = pd.read_excel(
        sciezka_pliku,
        skiprows=2,
        header=None
    )

    df = df.iloc[0:2,2:-1].T
    df = df.reset_index(drop=True)
    df = df.rename(columns={0 : 'dzien_miesiaca', 1 : 'dzien_tygodnia'})
    df["dzien_tygodnia"] = df["dzien_tygodnia"].replace({"cz": "czw"})

    return df

def wczytaj_rozklad_zajec_miesiac(sciezka_pliku_rozklad_zajec: str, sciezka_pliku_grafik: str) -> pd.DataFrame:
    '''
    Tworzy Dataframe będący rozkładem zajęc na cały miesiąc.
    Kombinacje dni misiąca i tygodnia brane są z dyspozycyjnośici pracowników.
    '''
    df_rozklad = wczytaj_rozklad_zajec(sciezka_pliku_rozklad_zajec)
    df_kalendarz = wczytaj_kalendarz(sciezka_pliku_grafik)

    df_final = (
        df_kalendarz
        .merge(
            df_rozklad,
            left_on="dzien_tygodnia",
            right_on="dzien",
            how="left"
        )
        .drop(columns="dzien")
        .dropna(subset=["nazwa_zajec"])
        .sort_values(["dzien_miesiaca", "czas"])
        .reset_index(drop=True)
    )

    return df_final