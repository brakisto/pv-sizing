from math import ceil
from classes.pv import PVProduction

class BatterySizing(PVProduction):

    def __init__(self, load, irr_data, fresnel_eff, tnoct, gamma, panel_power, num_panel,
                 inversor_eff, batt_volt, days_auto, dod, amp_hour_rating, nominal_voltage,
                 amb_temp_multiplier, **kwargs):
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
            inversor_eff: float
                Eficiencia del inversor obtenida de la hoja técnica.
            batt_volt: int
                Voltaje del banco de baterías.
            amb_temp_multiplier: float
                Multiplicador de temperatura dependiente de la temperatura mínima en invierno.
            days_auto: float
                Días de autonomía.
            dod: float
                dod de la batería obtenida de la hoja ténica.
            amp_hour_rating: float
                Amp-hour rating obtenido de la hoja ténica.
            nominal_voltage: int
                Voltaje [V] nominal del sistema.
            batt_volt: int
                Voltaje [V] de una batería.
        """
        super().__init__(load=load, irr_data=irr_data, fresnel_eff=fresnel_eff, tnoct=tnoct, gamma=gamma,
                         panel_power=panel_power, num_panel=num_panel,
                         lat=None, lon=None, start_date=None, end_date=None, tilt=None,
                         surface_azimuth=None, freq='1H')

        self.inversor_eff = inversor_eff
        self.batt_volt = batt_volt
        self.days_auto = days_auto
        self.dod = dod
        self.amp_hour_rating = amp_hour_rating
        self.nominal_voltage = nominal_voltage
        self.amb_temp_multiplier = amb_temp_multiplier

    def daily_ah(self):
        """

        Returns: float
            Amperios-hora diarios [Ah]

        """
        daily_energy = self.mean_hourly_load_data().AE_kWh.sum() * 1000  # Pasamos a Wh
        return (daily_energy / self.inversor_eff) / self.batt_volt

    def battery_sizing(self):
        """

        Returns: tuple
            Capcaidad total de baterías, número de baterías en paralelo, número de baterías en serie

        """
        daily_ah = self.daily_ah() * self.amb_temp_multiplier
        total_battery_capacity = (daily_ah * self.days_auto) / self.dod
        n_bat_paralell = ceil(total_battery_capacity / self.amp_hour_rating)
        n_bat_series = ceil(self.nominal_voltage / self.batt_volt)
        return total_battery_capacity, n_bat_paralell, n_bat_series
