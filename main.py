from cProfile import label
from pydoc import text
from re import X
from turtle import color
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.button import Button
# from kivy.uix.boxlist_view import Boxlist_view
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import bs4
import webbrowser
from bs4 import BeautifulSoup
# from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from kivymd.uix.fitimage import FitImage

from loginscreen import LoginScreen
from resultscreen import ResultScreen
from screenmanager import ScreenManager
"""
This is an example of kaki app usin kivymd modules.
"""
import os


from kivymd.app import MDApp
from kaki.app import App
from kivy.factory import Factory


# main app class for kaki app with kivymd modules
class LiveApp(MDApp, App):
    """ Hi Windows users """

    DEBUG = 1  # set this to 0 make live app not working

    # *.kv files to watch
    KV_FILES = {
        os.path.join(os.getcwd(), "screenmanager.kv"),
        os.path.join(os.getcwd(), "loginscreen.kv"),
        os.path.join(os.getcwd(), "resultscreen.kv"),

    }

    # class to watch from *.py files
    CLASSES = {
        "MainScreenManager": "screenmanager",
        "LoginScreen": "loginscreen",
        "ResultScreen": "resultscreen",
    }

    # auto reload path
    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def buttonClicked(self, login, senha, item):
        
        # login = 31240
        # senha = "2105_kasa"
        # item = "impeller"
        options = Options()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('window-size=200,400')
        
        # Abre o Navegador e Entra no Site
        navegador = webdriver.Chrome(chrome_options=options)
        navegador.get("https://portal.mercurymarine.com.br/epdv/epdv001.asp")
        # Insere o login e Senha
        navegador.find_element(
            By.XPATH, '/html/body/center/form/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/input').send_keys(login)
        navegador.find_element(
            By.XPATH, '/html/body/center/form/table/tbody/tr/td/table[2]/tbody/tr[3]/td[2]/input').send_keys(senha)
        navegador.find_element(
            By.XPATH, '/html/body/center/form/table/tbody/tr/td/table[2]/tbody/tr[4]/td/input').send_keys(Keys.ENTER)
        
        navegador.get(
            "https://portal.mercurymarine.com.br/epdv/epdv002d2.asp?s_nr_pedido_web=11111111111111111&s_nr_tabpre=&s_fm_cod_com=null&s_desc_item=" + item)
        sleep(4)
        
        """
        Verifica se o termo digitado esta correto ou foi encontrado
        
        """
        teste = navegador.find_element(
            By.XPATH, '/html/body/form[1]/table/tbody/tr/td/table[2]/tbody/tr[3]')
        
        if teste.get_attribute("class") == 'NoRecords':
            print('Nenhum registro encontrado - favor verificar !')
        else:
            print('Sucesso! item encontrado')
        
        # Pegar valor da pesquisa codigo  nome  valor custo e valor venda
        procura = navegador.page_source
        site = BeautifulSoup(procura, 'html.parser')
        
        linha = len(navegador.find_elements(
            By.XPATH, '//*[@id="preco_item_web"]/table/tbody/tr/td/table[2]/tbody/tr'))
        coluna = len(navegador.find_elements(
            By.XPATH, '//*[@id="preco_item_web"]/table/tbody/tr/td/table[2]/tbody/tr[3]/td'))
        
        # Print rows and columns
        # print(linha)
        
        coluna -= 1
        linha -= 1
        # itens = 0
        
        # table = np.empty((linha, coluna), int)
        # table1 = [1,2,3]
        lista = []
        descricao = []
        qtdaEst = []
        valor = 0
        valorTabela = []
        valorCusto = []
        for r in range(3, int(linha + 1)):
            for p in range(4, int(coluna + 1)):
                element = navegador.find_element(
                    By.XPATH,
                    '//*[@id="preco_item_web"]/table/tbody/tr/td/table[2]/tbody/tr[' + str(r) + ']/td[' + str(p) + ']')
                html_content = element.get_attribute('outerHTML')
                soup = BeautifulSoup(html_content, 'html.parser')
                table = soup.find('td')
                lista.append(soup.find('td').text)
        
                # print(table.text)
                valor = len(lista)
                valor = valor - 1
        # print(f'Encontrado {valor / 5}')
        

        dicionario = list()
        lista1 = dict()
        for i in range(0, valor, 5):
            lista1 = {
                'descricao': lista[i],
                'qtdaEst': lista[i+1],
                'valorVenda': lista[i +2],
                'valorTabela': lista[i+3],
                'valorCusto': lista[i+4],
                'qtdEncontrada': valor/5
                }
            dicionario.append(lista1.copy())
        #print(dicionario)

        # for e in dicionario:
        #     for v in e.values():
        #         print(v, end=' ')
        #         print('')
        print(dicionario[0].get("descricao"))
        return str(dicionario[0].get("descricao"))
                    
    def build_app(self):
        return Factory.MainScreenManager()


# finally, run the app
if __name__ == "__main__":
    LiveApp().run()
