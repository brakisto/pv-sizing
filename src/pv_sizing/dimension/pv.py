import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
import numpy_financial as npf
from itertools import accumulate
from collections import deque

from pv_sizing.utils.pv_utils import performance_ratio, european_efficiency_inverter, index_tuple_to_datetime, oneyear_todatetimeindex, \
                                    idae_pv_prod, cell_temp
from pv_sizing.utils.irradiance import get_irradiance

from pv_sizing.utils.constants import fresnel_fixed

import warnings
from pandas.core.common import SettingWithCopyWarning




warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


class PVProduction:

    def __init__(self, load, irr_data,  tnoct, gamma, panel_power, num_panel, fresnel_eff = fresnel_fixed,
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
            raise NotImplementedError('API is needed for hourly temperature')

        self.load = load
        self.irr_data = irr_data

        if len(self.load.columns) > 1:
            raise ValueError(f'DataFrame found with {len(self.load.columns)}, only 1 is needed.')

        if 'AE_kWh' not in self.load.columns.values:
            self.load.rename(columns={self.load.columns.values[0]: 'AE_kWh'}, inplace = True)

        if not isinstance(self.load.index, pd.DatetimeIndex) or not isinstance(self.load.index, pd.DatetimeIndex):
            try:
                self.load.index = pd.to_datetime(self.load.index)
                self.irr_data.index = pd.to_datetime(self.irr_data.index)
            except:
                raise TypeError('Index must be DateTimeIndex')
        
        self.fresnel_eff = fresnel_eff
        self.tnoct = tnoct
        self.gamma = gamma
        self.panel_power = panel_power
        self.num_panels = num_panel

        self.prod_data = self.pv_production()
        self.myload_yearly, self.myirr_yearly, self.myprod_yearly = self._yearly_load_and_irr_to_datetime_index()

    def mean_yearly_load_data(self):
        """
        Función para calcular la media anual de la carga.

        Returns: pd.DataFrame con la media anual de la carga
        """

        return oneyear_todatetimeindex(
            self.load.groupby([self.load.index.month, self.load.index.day, self.load.index.hour]).mean())

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
        return self.load.groupby([self.load.index.hour]).mean()

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
        Función para crear un Data Frame de irradiancia el Performance Ratio de la instalción y la producción de
        energía para cada time step.

        Returns: pd.DataFrame con producción horaria
        """

        df_prod = pd.DataFrame(index = self.irr_data.index)

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

        comprada = balance.loc[balance > 0].rename('from_grid')
        vertida = balance.loc[balance < 0].rename('into_grid')

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
        load = self.mean_yearly_load_data().AE_kWh.to_frame()

        if not isinstance(buy_price, (int, float, str)):

            if isinstance(buy_price, pd.DataFrame) and not isinstance(buy_price.index, pd.DatetimeIndex):
                try:
                    buy_price.index = pd.to_datetime(buy_price.index)
                except:
                    raise TypeError(f"Found type {type(buy_price.index)} but pd.DatetimeIndex was expected.")

            if len(buy_price) != 24:
                raise ValueError(f"{type(buy_price)} found with length {len(buy_price)} but 24 was expected.")

            while buy_price.index[0].hour != self.load.index[0].hour: #Rotamos la lista hasta que la primera hora del precio coincida con la primera hora de la carga.
                dq = deque(buy_price.index)
                dq.rotate(1)
                buy_price.index = dq

            lst_buy_price = buy_price.loc[:, buy_price.columns[0]].tolist()  #Pasamos a lista los valores del precio
            lst_buy_price *= len(load)//len(lst_buy_price) #Hacemos que la lista del precio coincida en longitud con el dataframe
            load['buy_price'] = lst_buy_price #Creamos la columna en el dataframe con el precio horario.

            total_df = pd.concat([load, comprada, vertida], axis=1).fillna(0) #Concatenamos la carga, energía comprada y vertida en un mismo DataFrame

            coste_energia_actual = sum(total_df.buy_price * total_df.AE_kWh)
            coste_energia_pv = sum(total_df.buy_price * total_df.from_grid)
            compensacion_pv = -sum(total_df.buy_price * total_df.into_grid)
        else:
            coste_energia_actual = sum(buy_price * load.AE_kWh)
            coste_energia_pv = sum(buy_price * comprada)
            compensacion_pv = -sum(sell_price * vertida)

        ahorro = coste_energia_actual - coste_energia_pv + compensacion_pv

        return coste_energia_actual, coste_energia_pv, compensacion_pv, ahorro

    def economic_analysis(self, init_inversion, buy_price=0.32, sell_price=0.06,ibi=None, oym_perc=0.02, proj_duration=25, ipc=0.04,
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
        ahorro = self.savings_from_pv(buy_price=buy_price, sell_price=sell_price)[-1]
        oym = init_inversion * oym_perc

        initial_inversion = np.zeros(len(years))
        initial_inversion[0] = init_inversion

        duration_project_savings = np.array([ahorro * ((1 + ipc) ** (year - 1)) for year in years])
        duration_project_oym = np.array([oym * ((1 + oym_perc) ** (year - 1)) for year in years])

        cf = - initial_inversion - duration_project_oym + duration_project_savings
        a_cf = np.array(list(accumulate(cf)))

        if ibi:
            raise ValueError('This option haven´t been added yet.')

        df_cf = pd.DataFrame(
            {'Initial inversion': initial_inversion, 'Operation and maintanence': duration_project_oym, 'Savings': duration_project_savings, 'Cashflow': cf,
             'Accumulated cashflow': a_cf})

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
        myload.AE_kWh.to_frame().rename(columns={'AE_kWh':'Load'}).plot(ax=ax[0])
        myprod.kWh.to_frame().rename(columns={'kWh':'Production'}).plot(ax=ax[0])

        ax[0].set(title = "Yearly photovoltaic production and load", ylabel="Energy [kWh]", xlabel="Time [hours]")
        ax[1].set(title = "Cashflow", xlabel="Time [years]", ylabel= "Money [€]")

        ax[0].legend()

        plt.tight_layout()
        plt.show()
