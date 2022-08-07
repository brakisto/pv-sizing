import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
import numpy_financial as npf
from itertools import accumulate

from utils.pv_utils import performance_ratio, european_efficiency_inverter, index_tuple_to_datetime, oneyear_todatetimeindex, \
                            remove_leap_day, remove25hformat, from24to00, idae_pv_prod, cell_temp
from utils.irradiance import get_irradiance

import warnings
from pandas.core.common import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def _correct_load_data(load):
    """_summary_

    Args:
        load (_type_): _description_

    Returns:
        _type_: _description_
    """

    # Corregimos los datos
    load = remove25hformat(load)
    load = from24to00(load)
    load.set_index('time', inplace=True)
    return load


def _correct_irr_data(irr):
    """_summary_

    Args:
        irr (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Pasamos los datos de fecha a format datetime.
    irr.index = pd.to_datetime(irr.index, format='%Y%m%d:%H%M', errors='coerce')
    # Quitamos 29 de Febrero si existe por comodidad
    irr = remove_leap_day(irr)
    return irr


class PVProduction:

    def __init__(self, load, irr_data, fresnel_eff, tnoct, gamma, panel_power, num_panel,
                 lat=None, lon=None, start_date=None, end_date=None, tilt=None,
                 surface_azimuth=None, freq='1H'):
        """
        Args:
            load: pd.DataFrame
                Datos horarios de carga obtenido de https://www.edistribucion.com/
            irr_data: pd.DataFrame
                Irradiancias (directa, difusa y reflejada) sobre el plano inclinado, temperatura
                media, velcodidad del viento horarios obtenido a partir de https://re.jrc.ec.europa.eu/pvg_tools/en/
            tnoct: int
                "Nominal operating cell temperature" facilitada por el fabricante
            gamma: float
                Coeficiente de pérdidas facilitado por el fabricante
            panel_power: int
                Potencia pico del panel fotovoltaico
            num_panel: int
                Número de paneles fotovoltaicos
            fresnel_eff: array_like
                Eficiencia fresnel por cada mes

        """

        if irr_data is None:
            self.irr_data = get_irradiance(lat, lon, start_date, end_date, tilt, surface_azimuth, freq)
            raise ValueError('Se necesita API para datos de temperatura horaria')

        self.load = _correct_load_data(load)
        self.irr_data = _correct_irr_data(irr_data)
        
        self.fresnel_eff = fresnel_eff
        self.tnoct = tnoct
        self.gamma = gamma
        self.panel_power = panel_power
        self.num_panels = num_panel

        self.prod_data = self.pv_production()

    def mean_yearly_load_data(self):
        """
        Función para calcular la media anual de la carga.

        Returns: pd.DataFrame con la media anual de la carga
        """

        return oneyear_todatetimeindex(
            self.load.groupby([self.load.index.month, self.load.index.day, self.load.Hora]).mean())

    def mean_yearly_irr_data(self):
        """
        Función para calcular la media anual de la irradiancia.

        Returns: pd.DataFrame con la media anual de la irradiancia
        """

        return oneyear_todatetimeindex(self.irr_data.groupby(
            [self.irr_data.index.month, self.irr_data.index.day, self.irr_data.index.hour]).mean())
    
    def mean_yearly_prod_data(self):
        """
        Función para calcular la media anual de la producción.

        Returns: pd.DataFrame con la media anual de la producción
        """

        return oneyear_todatetimeindex(self.prod_data.groupby(
            [self.prod_data.index.month, self.prod_data.index.day, self.prod_data.index.hour]).mean())
    
    def mean_hourly_load_data(self):
        """
        Función para calcular la media horaria de la carga.

        Returns: pd.DataFrame con la media horaria de la carga

        """
        return self.load.groupby([self.load.Hora]).mean()

    def mean_hourly_irr_data(self):
        """
        Función para calcular la media horaria de la irradiancia.

        Returns: pd.DataFrame con la media horaria de la irradiancia
        """
        return self.irr_data.groupby([self.irr_data.index.hour]).mean()

    def mean_hourly_irr_data(self):
        """
        Función para calcular la media horaria de la producción.

        Returns: pd.DataFrame con la media horaria de la producción
        """
        return self.prod_data.groupby([self.prod_data.index.hour]).mean()

    def pv_production(self):
        """
        Función para añadir al Data Frame de irradiancia el Performance Ratio de la instalción y la producción de
        energía para cada time step.

        """

        df_prod = pd.DataFrame(index = self.irr_data.index)

        # CÁLCULO DE LA ENERGÍA PRODUCIDA
        # IRRADIANCIA SUMA DIRECTA, DIFUSA Y REFLEJADA
        self.irr_data['Irr'] = self.irr_data['Gb(i)'] + self.irr_data['Gd(i)'] + self.irr_data['Gr(i)']

        df_prod = cell_temp(df_prod, self.irr_data, self.tnoct)
        df_prod = performance_ratio(df_prod, self.gamma, df_prod.T_cell, self.fresnel_eff.mean())
        df_prod = idae_pv_prod(df_prod, self.irr_data, self.panel_power, self.num_panels)

        return df_prod

    def _yearly_load_and_irr_to_datetime_index(self):
        """
        Función para convertir el índice de la media anual de irradiancia y carga a formato datetime.

        Returns: tuple
            Tupla con Data Frames con la carga e irradiancia anual

        """
        myload = self.mean_yearly_load_data().set_index(
            pd.date_range('2019-01-01', '2020-01-01', freq='H', inclusive='left'))
        myirr = self.mean_yearly_irr_data().set_index(
            pd.date_range('2019-01-01', '2020-01-01', freq='H', inclusive='left'))
        myprod = self.mean_yearly_prod_data().set_index(
            pd.date_range('2019-01-01', '2020-01-01', freq='H', inclusive='left'))
        return myload, myirr, myprod

    def energy_balance(self):
        """
        Función para calcular el balance energético anual.

        Returns: tuple
            Tupla con el balance energético, energía comprada y energía vertida.

        """
        df_prod = self.pv_production()

        myload, myirr, myprod = self._yearly_load_and_irr_to_datetime_index()
        balance = myload.AE_kWh - myprod.kWh

        comprada = balance.loc[balance > 0]
        vertida = balance.loc[balance < 0]

        return balance, comprada, vertida

    def savings_from_pv(self, buy_price=0.32, sell_price=0.06):

        """

        Args:
            buy_price: float
                Precio de compra de energía.
            sell_price: float
                Precio de venta de energía.

        Returns: tuple
            Tupla con el coste de energía sin producción fotovoltaica, coste de energía con producción fotovoltacia,
            ahorro por compensación de energía fotovoltacia y ahorro final.
        """

        balance, comprada, vertida = self.energy_balance()
        load = self.mean_yearly_load_data().AE_kWh

        coste_energia_actual = buy_price * load.sum()
        coste_energia_pv = buy_price * comprada.sum()
        compensacion_pv = -sell_price * vertida.sum()

        ahorro = coste_energia_actual - coste_energia_pv + compensacion_pv

        return coste_energia_actual, coste_energia_pv, compensacion_pv, ahorro

    def economic_analysis(self, init_inversion, ibi=None, oym_perc=0.02, proj_duration=25, ipc=0.04,
                          discount_rate=0.02):
        """

        Args:
            init_inversion: float
                Inversión inicial para la instalación.
            ibi: float
                Descuento dependiente del municipio en el que se haga la instalación.
            oym_perc: float
                Porcentaje de la inversión inicial equivalente a gastos en operación y mantenimiento.
            proj_duration: int
                Duración del proyecto.
            ipc: float
                Porecentaje correspondiente a la inflación y devaluación del dinero.
            discount_rate: float
                Coste de capital que se aplica para determinal el valor presente d eun pago futuro.


        Returns: tuple
            El primer valor corresponde a Data Frame con el cashflow, segundo valor corresponde a VAN y el último a TIR.

        """

        years = np.arange(1, proj_duration + 1)
        ahorro = self.savings_from_pv()[-1]
        oym = init_inversion * oym_perc

        initial_inversion = np.zeros(len(years))
        initial_inversion[0] = init_inversion

        duration_project_ahorro = np.array([ahorro * ((1 + ipc) ** (year - 1)) for year in years])
        duration_project_oym = np.array([oym * ((1 + oym_perc) ** (year - 1)) for year in years])

        cf = - initial_inversion - duration_project_oym + duration_project_ahorro
        a_cf = np.array(list(accumulate(cf)))

        if ibi:
            raise ValueError('No se ha añadido esta opción.')

        df_cf = pd.DataFrame(
            {'Inversión inicial': initial_inversion, 'OyM': duration_project_oym, 'Ahorro': duration_project_ahorro, 'Cashflow': cf,
             'Cashflow acumulado': a_cf})

        return df_cf, npf.npv(discount_rate, cf), npf.irr(cf)

    def plot(self, cashflow):
        """

        Args:
            cashflow: pd.DataFrame
                Data Frame con el cashflow acumulado del proyecto.

        """

        myload, myirr, myprod = self._yearly_load_and_irr_to_datetime_index()

        fig, ax = plt.subplots(2)
        cashflow.plot.bar(ax=ax[1])
        myload.AE_kWh.plot(ax=ax[0])
        myprod.kWh.plot(ax=ax[0])

        ax[0].set(title = "PV production and load", ylabel="Energy [kWh]", xlabel="Time [hours]")
        ax[1].set(title = "Cashflow", xlabel="Time [years]", ylabel= "Money [€]")

        plt.tight_layout()
        plt.show()
