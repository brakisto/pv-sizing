import pandas as pd

def european_efficiency_inverter(eta5, eta10, eta20, eta30, eta50, eta100):
    """
    Función para el cáculo de la Eficiencia Europea de un inversor.
    La Eficiencia Europea es una eficiencia de operación promedio
    sobre una distribución de energía anual correspondiente al clima
    de Europa Media y ahora se hace referencia en casi cualquier hoja de datos del inversor.

    El valor de esta eficiencia ponderada se obtiene asignando un porcentaje de tiempo a
    los residuos del inversor en un rango de funcionamiento dado.

    Suele venir en la hoja técnica del inversor.
    """
    return 0.03 * eta5 + 0.06 * eta10 + 0.13 * eta20 + 0.1 * eta30 + 0.48 * eta50 + 0.2 * eta100

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