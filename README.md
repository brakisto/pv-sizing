
[![Downloads](https://static.pepy.tech/personalized-badge/pv-sizing?period=total&units=international_system&left_color=black&right_color=blue&left_text=Downloads)](https://pepy.tech/project/pv-sizing)

# PV-sizing

**Please read the instructions carefully for the correct operation of the library. It is in an early stage of development and needs some improvements. However, its correct use gives very good results. Any help for the improvement and maintenance of the library is welcome!**

## Introduction

Photovoltaic sizing

This library allows the sizing of photovoltaic panels for any building and load curve provided. The photovoltaic producition was calculated using the "IDAE: Pliego de Condiciones Técnicas de Instalaciones Conectadas a Red" with the following equation:

$$
E_{\mathrm{p}}=\frac{G_{\mathrm{dm}}(\alpha, \beta) P_{\mathrm{mp}} P R}{G_{\mathrm{CEM}}}
$$

 By simply entering the number of panels (and their parameters from the datasheet provided by the manufacturer), the hourly irradiance (from https://re.jrc.ec.europa.eu/pvg_tools/en/), and the hourly load over a year it is possible to obtain the accumulated cahsflow taking into account the inflation over a period of 25 years (typical duration of a photovoltaic project). It is also necessary to provide the electricity purchase tariff, and also the price for compensation in case of grid feed-in.

It also allows the sizing of the battery bank for N days of autonomy based on the daily energy consumed.

The calculations for the initial investment have been calculated with typical market values. They can also be varied depending on the actual initial investment.

In the image you can see a representation of the final result obtained. Also in the table below the accumulated cashflow over the liftime of the project is shown.

| Year | Initial inversion | Operation and maintenence | Savings      | Cashflow     | Accumulated cashflow |
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

## Data structure

Irradiance and load must be hourly and must contain a minimum of **one full year of data**. If the data contains more than one year, the library automatically averages the available data over the year.

### Load data

| time                | Load (kWh) |
|---------------------|--------|
| 2020-07-01 01:00:00 | 0.206  |
| 2020-07-01 02:00:00 | 0.204  |
| 2020-07-01 03:00:00 | 0.197  |
| 2020-07-01 04:00:00 | 0.205  |
| 2020-07-01 05:00:00 | 0.196  |
| 2020-07-01 06:00:00 | 0.198  |
| 2020-07-01 07:00:00 | 0.196  |
| 2020-07-01 08:00:00 | 0.418  |
| 2020-07-01 09:00:00 | 0.187  |
| 2020-07-01 10:00:00 | 0.189  |
| 2020-07-01 11:00:00 | 0.19   |
| 2020-07-01 12:00:00 | 0.203  |
| 2020-07-01 13:00:00 | 0.19   |
| 2020-07-01 14:00:00 | 0.193  |
| 2020-07-01 15:00:00 | 0.191  |
| 2020-07-01 16:00:00 | 0.235  |
| 2020-07-01 17:00:00 | 0.197  |
| 2020-07-01 18:00:00 | 0.194  |
| 2020-07-01 19:00:00 | 0.189  |
| 2020-07-01 20:00:00 | 0.189  |
| 2020-07-01 21:00:00 | 0.207  |
| 2020-07-01 22:00:00 | 0.292  |
| 2020-07-01 23:00:00 | 0.298  |

### Irradiation data

| time                | Gb(i)  | Gd(i)  | Gr(i) | H_sun | T2m   | WS10m | Int |
|---------------------|--------|--------|-------|-------|-------|-------|-----|
| 2005-01-01 00:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 7.97  | 1.66  | 0.0 |
| 2005-01-01 01:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.42  | 1.79  | 0.0 |
| 2005-01-01 02:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.37  | 1.93  | 0.0 |
| 2005-01-01 03:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.35  | 2.0   | 0.0 |
| 2005-01-01 04:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.31  | 2.0   | 0.0 |
| 2005-01-01 05:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.12  | 1.86  | 0.0 |
| 2005-01-01 06:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 5.79  | 1.72  | 0.0 |
| 2005-01-01 07:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 5.75  | 1.93  | 0.0 |
| 2005-01-01 08:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 5.57  | 1.86  | 0.0 |
| 2005-01-01 09:09:00 | 181.33 | 57.09  | 1.71  | 12.55 | 6.39  | 1.86  | 0.0 |
| 2005-01-01 10:09:00 | 400.78 | 113.83 | 4.3   | 22.66 | 8.11  | 2.07  | 0.0 |
| 2005-01-01 11:09:00 | 611.53 | 135.72 | 6.6   | 30.96 | 9.2   | 2.28  | 0.0 |
| 2005-01-01 12:09:00 | 660.96 | 192.72 | 7.89  | 36.57 | 9.85  | 2.28  | 0.0 |
| 2005-01-01 13:09:00 | 710.3  | 211.02 | 8.59  | 38.61 | 10.18 | 2.14  | 0.0 |
| 2005-01-01 14:09:00 | 650.11 | 235.03 | 8.25  | 36.65 | 10.25 | 2.07  | 0.0 |
| 2005-01-01 15:09:00 | 670.37 | 184.76 | 7.57  | 31.1  | 10.12 | 2.07  | 0.0 |
| 2005-01-01 16:09:00 | 485.18 | 184.65 | 5.6   | 22.85 | 9.75  | 2.14  | 0.0 |
| 2005-01-01 17:09:00 | 0.0    | 72.22  | 1.09  | 12.76 | 9.08  | 2.21  | 0.0 |
| 2005-01-01 18:09:00 | 0.0    | 24.97  | 0.38  | 1.48  | 7.98  | 2.21  | 0.0 |
| 2005-01-01 19:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 7.19  | 2.41  | 0.0 |
| 2005-01-01 20:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.67  | 2.62  | 0.0 |
| 2005-01-01 21:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.29  | 2.76  | 0.0 |
| 2005-01-01 22:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 6.03  | 2.97  | 0.0 |
| 2005-01-01 23:09:00 | 0.0    | 0.0    | 0.0   | 0.0   | 5.82  | 3.17  | 0.0 |

Gb(i): Beam (direct) irradiance on the inclined plane (plane of the array) (W/m2)
Gd(i): Diffuse irradiance on the inclined plane (plane of the array) (W/m2)
Gr(i): Reflected irradiance on the inclined plane (plane of the array) (W/m2)
H_sun: Sun height (degree)
T2m: 2-m air temperature (degree Celsius)
WS10m: 10-m total wind speed (m/s)
Int: 1 means solar radiation values are reconstructed

This CSV file can be obtained with the PVGIS class explained below.

### Electricity price

For electricity price data you can provide a fixed price, or a format as shown in the table below. **It needs to be a DataFrame with the index of type DatetimeIndex in order to automatically match the first hour of the load DataFrame and the electricity price DataFrame.  Only the prices for 24 hours must be provided.**

| Hour                | €/kWh   |
|---------------------|---------|
| 2022-04-09 00:00:00 | 0.33419 |
| 2022-04-09 01:00:00 | 0.33143 |
| 2022-04-09 02:00:00 | 0.33193 |
| 2022-04-09 03:00:00 | 0.34965 |
| 2022-04-09 04:00:00 | 0.35213 |
| 2022-04-09 05:00:00 | 0.34960 |
| 2022-04-09 06:00:00 | 0.36944 |
| 2022-04-09 07:00:00 | 0.37212 |
| 2022-04-09 08:00:00 | 0.36155 |
| 2022-04-09 09:00:00 | 0.29125 |
| 2022-04-09 10:00:00 | 0.17853 |
| 2022-04-09 11:00:00 | 0.14803 |
| 2022-04-09 12:00:00 | 0.13411 |
| 2022-04-09 13:00:00 | 0.13434 |
| 2022-04-09 14:00:00 | 0.11547 |
| 2022-04-09 15:00:00 | 0.07960 |
| 2022-04-09 16:00:00 | 0.06471 |
| 2022-04-09 17:00:00 | 0.05458 |
| 2022-04-09 18:00:00 | 0.13163 |
| 2022-04-09 19:00:00 | 0.19826 |
| 2022-04-09 20:00:00 | 0.29412 |
| 2022-04-09 21:00:00 | 0.34978 |
| 2022-04-09 22:00:00 | 0.35915 |
| 2022-04-09 23:00:00 | 0.35213 |

## Install

PV-sizing depends on the following libraries:

- pandas
- numpy
- numpy-financial

Optional libraries:

- pvlib
- selenium
- plotly
- dash

To install the library you can simply use the pip command as follows:

```
pip install pv-sizing
```

## Example photovoltaic production

```
from pv_sizing.dimension.pv import PVProduction

from pv_sizing.utils.load_example import example_irr, example_load

from pv_sizing.utils.constants import fresnel_fixed
from pv_sizing.utils.pv_utils import init_inv

from pv_sizing.web_scrapping.electricity_price import ElectricityPrice

import pandas as pd


pv_costs = {"num_panel": 5,
            "price_panel": 260,
            "price_inverter" : 1300,
            "additional_cost" : 500,
            "installation_cost_perc" : 0.15}

initial_investment = init_inv(**pv_costs)

electricity_price = ElectricityPrice().extract_data()

pv = PVProduction(irr_data=example_irr, load=example_load, tnoct=42, gamma=-0.36, 
                    panel_power=450, num_panel=num_panel, fresnel_eff=fresnel_fixed)

cashflow, van, tir = pv.economic_analysis(initial_investment, sell_price=0.06, buy_price=electricity_price)

pv.plot(cashflow['Accumulated cashflow'])

```

### Example battery sizing

```
from pv_sizing.dimension.battery import BatterySizing
from pv_sizing.utils.load_example import example_irr, example_load

days_auto = 0.5

bat = BatterySizing(irr_data=example_irr, load=example_load, tnoct=42, gamma=-0.36, 
                    panel_power=450, num_panel=num_panel,fresnel_eff=fresnel_fixed,
                    amb_temp_multiplier=1.163, days_auto=days_auto, dod=0.95,
                    amp_hour_rating= 2400 / 48, batt_volt=48, inversor_eff=0.85)

total_battery_capacity, n_bat_paralell, n_bat_series = bat.battery_sizing()
```

## Example PVGIS scrapping

```
from pv_sizing.web_scrapping.irradiance import PVGIS
import os

pvgis = PVGIS(lat = 28.242, lon = -16.647, azimuth = 0, elevation = 30, absolute_path = os.getcwd())
pvgis.interact_with_page()

```

*Some other files may be necessary for the correct functioning of this class. Currently it is necessary to use Chrome with ChromeDriver 103.0.5060.134. The location in the machine is no relevant since the webdriver_manager is used in the script.


## Example of electricity price scrapping

This class allows the extraction of hourly energy prices. The prices have been obtained from the Spanish Electricity Grid (REE) for the day of execution of the script.

```
from pv_sizing.web_scrapping.electricity_price import ElectricityPrice

electricity_price = ElectricityPrice().extract_data()
```

*Some other files may be necessary for the correct functioning of this class. Currently it is necessary to use Chrome with ChromeDriver 103.0.5060.134. The location in the machine is no relevant since the webdriver_manager is used in the script.

## Example interactive plot

```
from pv_sizing.app_layout.dashboard import interactive_plot
from pv_sizing.app_layout.applayout import app

interactive_plot()

if __name__ == "__main__":
    app.run_server(debug=True)
```

When this code has been run, the following message will appear in the terminal:

Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'pv_sizing.app_layout.applayout'
 * Debug mode: on

Open http://127.0.0.1:8050/ on your terminal and try the interactive sizing mode.

In this version, only the example data can be used for the interactive plot. In future versions it will be possible to drag the load and irradiance .CSV files directly into the browser. 

![](https://github.com/brakisto/PV-sizing/raw/main/src/imgs/interactive_plot.png)
