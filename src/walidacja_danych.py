import pandas as pd


def sprawdz_kolumny(df: pd.DataFrame) -> bool:
    dozwolone_schematy = [['pracownik', 'specjalizacja', 'nazwa_zajec', 'rola', 'udział'],
                          ['dzien', 'czas', 'sala', 'nazwa_zajec']]

    if list(df.columns) in dozwolone_schematy:
        return True

    if df.columns[0] == ('dzień miesiąca', 'dzień tygodnia'):
        #print('Dni miesiąca zgadzają się')
        if  29 <= len(df.columns) <= 32: #od 29 do 32, bo na początku jest jeszcze kolumna z ('dzień miesiąca', 'dzień tygodnia')
            #print('ilość dni miesiąca zgadza się')
            week_days = ['pn', 'wt', 'śr', 'cz', 'pt', 'sb', 'nd']
            for i in range(2,len(df.columns)):
                prev_day = df.columns[i-1]
                curr_day = df.columns[i]
                cond_month_days = prev_day[0] == (curr_day[0] - 1)
                cond_week_days = prev_day[1] ==  week_days[week_days.index(curr_day[1]) - 1]
                if not (cond_month_days & cond_week_days):
                    #print(f'cond_month_days: {cond_month_days}, cond_week_days: {cond_week_days}')
                    return False
            return True
    #print('Final False')
    return False

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

