from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

class PVGIS():
    def __init__(self, lat, lon, azimuth, elevation, absolute_path):

        """Clase para hace scrapping de la página web de PVGIS 

        Args:
            lat (float): Latitud del lugar
            lon (float): Longitud del lugar
            azimuth (float): Azimuth de -180º a 180º
            elevation (float): Elevación de 0º a 90º
            absolute_path (string): Dirección absoluta de donde guardar el archivo
            
        """

        self.lat = lat
        self.lon = lon
        self.azimuth = azimuth
        self.elevation = elevation

        self.prefs = {'download.default_directory' : absolute_path}
        self.co = webdriver.ChromeOptions()
        self.co.add_experimental_option('prefs', self.prefs)
        self.driver = webdriver.Chrome(chrome_options=self.co,executable_path=ChromeDriverManager().install())
    
    def interact_with_page(self):
        """Función para interactuar con la página web de PVGIS
        """

        #Vamos a la página para los tramos horarios.
        url  = f'https://re.jrc.ec.europa.eu/pvg_tools/en/#HR'
        self.driver.get(url)
        
        #Seleccionamos latitud y longitud.
        latitude =  WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "inputLat")))
        longitude =  WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "inputLon")))

        latitude.send_keys(f'{self.lat}')
        longitude.send_keys(f'{self.lon}')

        go_buttons = self.driver.find_elements(By.ID, "tr_go")
        go_buttons[-1].click()
        time.sleep(2)

        #Seleccionamos azimuth y elevación.
        slope =  WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "hourlyangle")))
        azimuth =  WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "hourlyaspect")))

        slope.send_keys(f'{self.elevation}')
        azimuth.send_keys(f'{self.azimuth}')
        # time.sleep(2)

        #Seleccionamos componentes de radiación.
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='components']"))).click()
        # time.sleep(2)

        #Descargamos los datos seleecionados.
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='hourlydownloadcsv']"))).click()
