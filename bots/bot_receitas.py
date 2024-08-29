import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import requests


class RevenueBot:
    """
    Bot para baixar os dados de receitas do Portal da Transparência.
    """

    def __init__(self, web_url: str, download_time: int):
        self.donwload_folder = f"{os.getcwd()}/csv/"
        self.url = web_url
        self.download_wait_time = download_time
        
        chrome_options = ChromeOptions()
        prefs = {'download.default_directory': self.donwload_folder}
        chrome_options.add_experimental_option('prefs', prefs)

        self.driver = Chrome(options=chrome_options)
        self.clear_folder()

    @staticmethod
    def get_status(web_url: str):
        """
        Retorna o status da página.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            
            response = requests.get(web_url, headers=headers)
            
            if response.status_code == 200:
                return "Status da Página: Online"
            else:
                return f"Status da Página: Offline. Código de status: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"A página está offline. Erro: {e}"

    def clear_folder(self):
        """
        Limpa a pasta de downloads (csv) se ela não estiver vazia.
        """
        if len(os.listdir(self.donwload_folder)) > 0:
            for file in os.listdir(self.donwload_folder):
                os.remove(os.path.join(self.donwload_folder, file))
                
    def start(self):
        """
        Inicia o bot para baixar o arquivo de receitas.
        """
        self.driver.get(self.url)
        desp_receitas = self.driver.find_element(By.ID, 'despesas-card')
        desp_receitas.click()

        receitas_consulta = self.driver.find_element(By.CSS_SELECTOR, '#receitas-links')
        consultas_link = receitas_consulta.find_elements(By.TAG_NAME, 'a')[1]
        consultas_link.click()

        tabela_opcoes = self.driver.find_element(By.CLASS_NAME, 'box-tabela-completa__opcoes')
        baixar_link = tabela_opcoes.find_elements(By.TAG_NAME, 'a')[1]
        baixar_link.click()

        sleep(self.download_wait_time)

        self.driver.quit()
