from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os

class WebScraper:
    def __init__(self, driver_path: str = None):
        options = Options()
        options.add_argument('--headless')
        if driver_path:
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Firefox(service=service, options=options)
        else:
            self.driver = webdriver.Firefox(options=options)

    def fetch_precio_compra(self, url: str) -> str:
        self.driver.get(url)
        time.sleep(5)

        try:
            element = self.driver.find_element(By.CSS_SELECTOR, 'p.bg-secondary')
            text = element.text
        except Exception:
            raise ValueError('No se encontró el elemento de precio de compra')

        match = re.search(r"([0-9]+(?:[\.,][0-9]+)?)", text)
        if not match:
            raise ValueError(f'Texto inesperado: {text}')

        precio = match.group(1).replace(',', '.')
        return precio

    def __del__(self):
        try:
            self.driver.quit()
        except:
            pass