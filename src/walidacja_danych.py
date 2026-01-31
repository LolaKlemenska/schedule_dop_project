from pandas.core.interchange.dataframe_protocol import DataFrame


def sprawdz_kolumny(df: DataFrame) -> bool:
    dozwolone_schematy = [['pracownik', 'specjalizacja', 'nazwa_zajec', 'rola', 'udział'],
                          ['dzien', 'czas', 'sala', 'nazwa_zajec']]

    if list(df.columns) in dozwolone_schematy:
        return True

    if df.columns[0] == ('dzień miesiąca', 'dzień tygodnia'):
        if  28 <= len(df.columns) <= 31:
            #dni_tygodnia = ['pn', 'wt', 'śr', 'cz', 'pt', 'sb', 'nd']
            for i in range(2,len(df.columns)):
                cond1 = (df.columns[i-1] + 1) == df.columns[i]
                if not cond1:
                    return False
            return True
    return False



