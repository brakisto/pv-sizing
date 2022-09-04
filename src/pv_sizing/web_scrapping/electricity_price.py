from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import datetime
import numpy as np
import pandas as pd


class ElectricityPrice():


    def __init__(self):

        """Clase para la extracción de los precios proporcionado por Red Eléctrica de España
        por tramos horarios.
        """

        self.co = webdriver.ChromeOptions()
        self.co.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=self.co,executable_path=ChromeDriverManager().install())

    def extract_data(self, index_to_datetime = True):
        """Método para la extracción del DataFrame

        Arg:
            index_to_datetime (bool): Poner a True si queremos el índice en formateo DateTime.

        Returns:
            pd.DataFrame: Archivo con precios de electricidad por tramos horarios.
        """
        
        url  = 'https://tarifaluzhora.es/'
        self.driver.get(url)

        times = self.driver.find_elements(By.XPATH, "//div//span[@itemprop='description']") 
        prices = self.driver.find_elements(By.XPATH, "//div//span[@itemprop='price']")

        if index_to_datetime:
            times = list(map(lambda x: datetime.time(int(x.text.split('h')[0])), times))
            date = pd.to_datetime(datetime.datetime.today().strftime("%d/%m/%Y"))
            time = list(map(lambda x: datetime.datetime.combine(date, x) ,times))
        else:
            time = list(map(lambda x: x.text, times))
                
        price = list(map(lambda x: float(x.text.split(' ')[0]), prices))
        unit = prices[0].text.split(' ')[-1]

        df = pd.DataFrame({f'{unit}': pd.Series(price, dtype=float), 'Hour': pd.Series(time, dtype=str)}).set_index('Hour', drop=True)

        return df



