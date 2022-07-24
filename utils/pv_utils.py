import pandas as pd

def index_tuple_to_datetime(df):
    a = pd.DataFrame(df.index.values.tolist(), columns=['month', 'day', 'hour'])
    df['time'] = pd.to_datetime(a, format='%m%d%H')
    return df

def init_inv(num_panel, price_panel, costes_adicionales, coste_instalacion, price_inverter):
    inversion_inicial = num_panel*price_panel + price_inverter + coste_instalacion + costes_adicionales
    return inversion_inicial + inversion_inicial*coste_instalacion

def oneyear_todatetimeindex(df):
    if not isinstance(df, pd.DataFrame):
        df = df.to_frame()
    return df.set_index(pd.date_range('2019-01-01', '2020-01-01', freq='H', inclusive='left'))

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

    Args:
        load:

    Returns:

    """
    load['Hora'] = load['Hora'].apply(
        lambda x: '0' + str(x) if len(str(x)) == 1 else x).astype(str)
    load['time'] = load['Fecha'].astype(str) + '-' + load['Hora']
    load['time'] = pd.to_datetime(load['time'], format='%d/%m/%Y-%H')
    return load