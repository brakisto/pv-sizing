# PV-sizing
Photovoltaic sizing

This library allows the sizing of photovoltaic panels for any building and load curve provided. By simply entering the number of panels (and their parameters from the datasheet provided by the manufacturer) it is possible to obtain the accumulated cahsflow and cashflow taking into account the infaltion over a period of 25 years (typical duration of a photovoltaic project). It is also necessary to provide the electricity purchase tariff, and also the price for compensation in case of grid feed-in.

It also allows the sizing of the battery bank for N days of autonomy based on the daily energy consumed.

The calculations for the initial investment have been calculated with typical market values. They can also be varied depending on the actual initial investment.

In the image you can see a representation of the final result obtained.

![alt text](imgs/pvprod.png?raw=true "(1) PV production and load; (2) Cashflow")
