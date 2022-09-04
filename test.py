from src.pv_sizing.dimension.pv import PVProduction
from src.pv_sizing.utils.load_example import example_irr, example_load

from src.pv_sizing.utils.constants import fresnel_fixed
from src.pv_sizing.utils.pv_utils import init_inv


from src.pv_sizing.web_scrapping.electricity_price import ElectricityPrice


electricity_price = ElectricityPrice().extract_data()

pv_costs = {"num_panel": 5,
            "price_panel": 260,
            "price_inverter" : 1300,
            "additional_cost" : 500,
            "installation_cost_perc" : 0.15}

initial_investment = init_inv(**pv_costs)

pv = PVProduction(irr_data=example_irr, load=example_load, tnoct=42, gamma=-0.36, 
                    panel_power=450, num_panel=5, fresnel_eff=fresnel_fixed)

cashflow, van, tir = pv.economic_analysis(initial_investment, sell_price=0.06,buy_price=electricity_price)

pv.plot(cashflow['Accumulated cashflow'])

