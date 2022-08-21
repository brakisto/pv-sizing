from pv_sizing.dimension.pv import PVProduction
from pv_sizing.dimension.battery import BatterySizing

from pv_sizing.utils.load_example import example_irr, example_load

from pv_sizing.utils.constants import fresnel_fixed
from pv_sizing.utils.pv_utils import init_inv

days_auto = 0.5
num_panel = 5
price_panel = 260
price_inverter = 1300
additional_cost = 500
installation_cost_perc = 0.15


initial_investment = init_inv(num_panel=num_panel, price_panel=price_panel,
                                additional_cost=additional_cost, installation_cost_perc=installation_cost_perc,
                                price_inverter=price_inverter)

pv = PVProduction(irr_data=example_irr, load=example_load, tnoct=42, gamma=-0.36, panel_power=450, num_panel=num_panel,
                    fresnel_eff=fresnel_fixed)

bat = BatterySizing(irr_data=example_irr, load=example_load, tnoct=42, gamma=-0.36, panel_power=450, num_panel=num_panel,
                    fresnel_eff=fresnel_fixed, amb_temp_multiplier=1.163, days_auto=days_auto, dod=0.95,
                    amp_hour_rating=2400 / 48, nominal_voltage=48, batt_volt=48, inversor_eff=0.85)

total_battery_capacity, n_bat_paraleirradiation, n_bat_series = bat.battery_sizing()
daily_load_Wh = pv.mean_hourly_load_data().AE_kWh.sum() * 1000  # to a Wh

coste_energia_actual, coste_energia_pv, compensacion_pv, savings = pv.savings_from_pv(sell_price=0.06,
                                                                                        buy_price=0.32)
cashflow, van, tir = pv.economic_analysis(initial_investment)

pv.plot(cashflow['Cashflow acumulado'])