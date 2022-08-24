def remove_leap_day(df):
    """

    Args:
        df:

    Returns:

    """
    return df[~((df.index.month == 2) & (df.index.day == 29))]

def remove_last_row(df):
    """

    Args:
        df:

    Returns:

    """
    return df[df.Fecha != 0]

def remove25hformat(load):
    """

    Args:
        load:

    Returns:

    """

    load = load.loc[load.Hora <= 24]
    load.loc[load.Hora == 24, 'Hora'] = 0
    load = remove_last_row(load)

    load['Hora'] = load['Hora'].apply(
        lambda x: '0' + str(x) if len(str(x)) == 1 else x).astype(str)

    load['time'] = load['Fecha'].astype(str) + '-' + load['Hora']
    load['time'] = pd.to_datetime(load['time'], format='%d/%m/%Y-%H')
    return load

def from24to00(load):
    """
    Función para pasar de 24:00 a 00:00 y así coincidior con 

    Args:
        load:

    Returns:

    """
    load['Hora'] = load['Hora'].apply(
        lambda x: '0' + str(x) if len(str(x)) == 1 else x).astype(str)
    load['time'] = load['Fecha'].astype(str) + '-' + load['Hora']
    load['time'] = pd.to_datetime(load['time'], format='%d/%m/%Y-%H')
    return load