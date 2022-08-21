import pandas as pd

def cell_temp(df_prod, irr_data, tnoct):
    """_summary_

    Args:
        df_prod (_type_): _description_
        irr_data (_type_): _description_
        tnoct (_type_): _description_

    Returns:
        _type_: _description_
    """
    # TEMPERATURA CÉLULA
    df_prod['T_cell'] = irr_data['T2m'] + irr_data['Irr'] * (tnoct - 20) / 800
    return df_prod

def idae_pv_prod(df_prod, df_irr, panel_power, num_panels):

    """_summary_

    Args:
        df_prod (_type_): _description_
        df_irr (_type_): _description_
        panel_power (_type_): _description_
        num_panels (_type_): _description_

    Returns:
        _type_: _description_
    """
    # PRODUCCION
    df_prod['Wh'] = df_prod['PR'] * df_irr['Irr'] * panel_power * num_panels / 1000 # E = GR [kW/m2] * PR * P [W] * num_panels / 1 kW/m2 /// Como son intervalos de 1 hora obtenemos Wh 
    df_prod['kWh'] = df_prod.Wh / 1e3
    df_prod['MWh'] = df_prod.Wh / 1e6
    return df_prod

def performance_ratio(df_prod_hourly, gamma, t_cell_hourly, mean_fresnel_eff):
    """_summary_

    Args:
        df_prod_hourly (pd.DataFrame): _description_
        gamma (float): _description_
        t_cell_hourly (numpy.array or pd.Series or pd.DataFrame): _description_
        mean_fresnel_eff (float): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    # PERFORMANCE RATIO
    df_prod_hourly['PRtemp'] = (1 + gamma * (t_cell_hourly - 25) / 100)

    # OBTENIDO A PARTIR DE LA FUNCIÓN PARA LA EFICIENCIA EUROPEA
    df_prod_hourly['PRfres'] = mean_fresnel_eff
    # CAIDA DE TENSIÓN DE 0,8% PARA CC
    df_prod_hourly['PRCC'] = 0.992
    df_prod_hourly['PRdisp'] = 1
    df_prod_hourly['PRCC/CA'] = european_efficiency_inverter(eta5=60, eta10=80, eta20=89, eta30=91, eta50=92,
                                                            eta100=93) / 100
    # CAIDA DEL 1,5% PARTE AC
    df_prod_hourly['PRAC'] = 0.985
    df_prod_hourly['PR'] = df_prod_hourly['PRtemp'] * df_prod_hourly['PRfres'] * df_prod_hourly['PRdisp'] * \
                            df_prod_hourly['PRCC'] * df_prod_hourly['PRCC/CA'] * df_prod_hourly['PRAC']
    
    return df_prod_hourly


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