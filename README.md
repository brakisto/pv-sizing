## PV-sizing

# Introduction

Photovoltaic sizing

This library allows the sizing of photovoltaic panels for any building and load curve provided. The photovoltaic producition was calculated using the "IDAE: Pliego de Condiciones Técnicas de Instalaciones Conectadas a Red" with the following equation:

$$
E_{\mathrm{p}}=\frac{G_{\mathrm{dm}}(\alpha, \beta) P_{\mathrm{mp}} P R}{G_{\mathrm{CEM}}}
$$

 By simply entering the number of panels (and their parameters from the datasheet provided by the manufacturer), the hourly irradiance (from https://re.jrc.ec.europa.eu/pvg_tools/en/), and the hourly load over a year it is possible to obtain the accumulated cahsflow taking into account the inflation over a period of 25 years (typical duration of a photovoltaic project). It is also necessary to provide the electricity purchase tariff, and also the price for compensation in case of grid feed-in.

It also allows the sizing of the battery bank for N days of autonomy based on the daily energy consumed.

The calculations for the initial investment have been calculated with typical market values. They can also be varied depending on the actual initial investment.

In the image you can see a representation of the final result obtained. Also in the table below the accumulated cashflow over the liftime of the project is shown.

| Año | Inversión inicial | OyM        | Ahorro      | Cashflow     | Cashflow acumulado |
|-----|-------------------|------------|-------------|--------------|--------------------|
| 0   | 3565.1725         | 71.303450  | 527.383444  | -3109.092506 | -3109.092506       |
| 1   | 0.0000            | 72.729519  | 548.478782  | 475.749263   | -2633.343243       |
| 2   | 0.0000            | 74.184109  | 570.417933  | 496.233824   | -2137.109419       |
| 3   | 0.0000            | 75.667792  | 593.234651  | 517.566859   | -1619.542560       |
| 4   | 0.0000            | 77.181147  | 616.964037  | 539.782889   | -1079.759671       |
| 5   | 0.0000            | 78.724770  | 641.642598  | 562.917828   | -516.841843        |
| 6   | 0.0000            | 80.299266  | 667.308302  | 587.009036   | 70.167193          |
| 7   | 0.0000            | 81.905251  | 694.000634  | 612.095383   | 682.262576         |
| 8   | 0.0000            | 83.543356  | 721.760659  | 638.217303   | 1320.479879        |
| 9   | 0.0000            | 85.214223  | 750.631086  | 665.416863   | 1985.896742        |
| 10  | 0.0000            | 86.918508  | 780.656329  | 693.737822   | 2679.634563        |
| 11  | 0.0000            | 88.656878  | 811.882582  | 723.225705   | 3402.860268        |
| 12  | 0.0000            | 90.430015  | 844.357886  | 753.927870   | 4156.788138        |
| 13  | 0.0000            | 92.238616  | 878.132201  | 785.893585   | 4942.681724        |
| 14  | 0.0000            | 94.083388  | 913.257489  | 819.174101   | 5761.855825        |
| 15  | 0.0000            | 95.965056  | 949.787789  | 853.822733   | 6615.678558        |
| 16  | 0.0000            | 97.884357  | 987.779300  | 889.894943   | 7505.573501        |
| 17  | 0.0000            | 99.842044  | 1027.290472 | 927.448428   | 8433.021929        |
| 18  | 0.0000            | 101.838885 | 1068.382091 | 966.543206   | 9399.565136        |
| 19  | 0.0000            | 103.875663 | 1111.117375 | 1007.241712  | 10406.806848       |
| 20  | 0.0000            | 105.953176 | 1155.562070 | 1049.608894  | 11456.415742       |
| 21  | 0.0000            | 108.072239 | 1201.784553 | 1093.712313  | 12550.128055       |
| 22  | 0.0000            | 110.233684 | 1249.855935 | 1139.622251  | 13689.750306       |
| 23  | 0.0000            | 112.438358 | 1299.850172 | 1187.411814  | 14877.162120       |
| 24  | 0.0000            | 114.687125 | 1351.844179 | 1237.157054  | 16114.319174       |

![](https://github.com/brakisto/PV-sizing/raw/main/src/imgs/pvprod.png)


# Install

PV-sizing depends on the following libraries:

- pandas
- numpy
- numpy-financial
- pvlib

To install the library you can simply use the pip command as follows:

```
pip install pv-sizing
```

# Example

```

from pv_sizing.dimension.pv import PVProduction
from pv_sizing.dimension.battery import BatterySizing

from pv_sizing.utils.load_example import example_irr, example_load

from pv_sizing.utils.constants import fresnel_fixed
from pv_sizing.utils.pv_utils import init_inv

days_auto = 0.5
num_panel = 5
price_panel = 260
price_inverter = 1300
add_cost = 500
coste_instalacion = 0.15


inversion_inicial = init_inv(num_panel=num_panel, price_panel=price_panel,
                                costes_adicionales=add_cost, coste_instalacion=coste_instalacion,
                                price_inverter=price_inverter)

pv = PVProduction(irr_data=example_irr, load=example_load, tnoct=42, gamma=-0.36, panel_power=450, num_panel=num_panel,
                    fresnel_eff=fresnel_fixed)

bat = BatterySizing(irr_data=example_irr, load=example_load, tnoct=42, gamma=-0.36, panel_power=450, num_panel=num_panel,
                    fresnel_eff=fresnel_fixed, amb_temp_multiplier=1.163, days_auto=days_auto, dod=0.95,
                    amp_hour_rating=2400 / 48, nominal_voltage=48, batt_volt=48, inversor_eff=0.85)

total_battery_capacity, n_bat_paraleirradiation, n_bat_series = bat.battery_sizing()
daily_load_Wh = pv.mean_hourly_load_data().AE_kWh.sum() * 1000  # to a Wh

coste_energia_actual, coste_energia_pv, compensacion_pv, ahorro = pv.savings_from_pv(sell_price=0.06,
                                                                                        buy_price=0.32)
cashflow, van, tir = pv.economic_analysis(inversion_inicial)

pv.plot(cashflow['Cashflow acumulado'])

```