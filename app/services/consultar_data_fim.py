from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
from dotenv import load_dotenv
import pyodbc
from multiprocessing import Process, Queue
from queue import Empty
import pandas as pd
from app.utils.selenium_utils import send_keys
data_agora = datetime.now()
date_format = f"%d/%m/%Y"

load_dotenv()

def buscar_rh_fim ():
    connection_string = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\01780742177\\Documents\\BaseDeclaracaoPisoPGE.accdb;"
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    data_analise = datetime.strptime("01/01/2017","%d/%m/%Y")
    rows = cursor.execute(f"SELECT cpf, vinculo FROM ResultadoBuscarVinculos WHERE data_fim IS NULL").fetchall()

    browser = webdriver.Chrome()
    browser.get("https://aplicacoes.expresso.go.gov.br/")
    browser.minimize_window()
    browser.implicitly_wait(10)
    wait = WebDriverWait(browser, 10)
    browser.find_element(By.NAME, "usernameUserInput").send_keys(os.getenv('ACESSO_RHNET'))
    browser.find_element(By.NAME,"password").send_keys(os.getenv('SENHA_RHNET'))
    browser.find_element(By.XPATH,"//*[@id='loginForm']/button").click()

    for i in range(1, 101):
        div = browser.find_element(By.XPATH,"/html/body/app-root/app-main/div/div/div/app-sistemas/div/p-dataview/div/div[2]/div/div[" + str(i) + "]").text

        if "RHNet" in div:
            browser.find_element(By.XPATH,"/html/body/app-root/app-main/div/div/div/app-sistemas/div/p-dataview/div/div[2]/div/div[" + str(i) + "]").click()
            break

    browser.switch_to.frame("principal")
    browser.execute_script("arguments[0].click();", browser.find_elements(By.XPATH, '//*[text()="Vínculo"]')[1])
    for dado in rows:
        send_keys(browser,(By.NAME,"txtCPF"),dado.cpf)
        browser.find_element(By.XPATH,"//input[@value='Pesquisar CPF']").click()
        time.sleep (.3)
        tabela = browser.find_element(By.XPATH,"/html/body/form/table[2]")
        linhas = tabela.find_elements(By.TAG_NAME, "tr")
        flag_encontrou = False
        for linha in linhas:
            if flag_encontrou:
                break
            browser.implicitly_wait(1)
            colunas = linha.find_elements(By.TAG_NAME, "td")
            browser.implicitly_wait(10)
            if len(colunas) == 8:
                if colunas[3].text == dado.vinculo:
                    if colunas[6].text == 'Desativado':
                        colunas[0].click()
                        browser.find_element(By.NAME, "Consultar").click()
                        dd = browser.find_element(By.NAME, "txtDataExclusaoDia").get_attribute("value")
                        mm = browser.find_element(By.NAME, "txtDataExclusaoMes").get_attribute("value")
                        yyyy = browser.find_element(By.NAME, "txtDataExclusaoAno").get_attribute("value")
                        data_fim = datetime.strptime(f"{dd}/{mm}/{yyyy}", "%d/%m/%Y")
                        browser.execute_script("arguments[0].click();", browser.find_elements(By.XPATH, "//input[@value='Cancelar']")[1])

                    else:
                        data_fim = datetime.now()
                    cursor.execute(f"""
                        UPDATE 
                            ResultadoBuscarVinculos 
                        SET
                            data_fim = #{datetime.strftime(data_fim,"%d/%m/%Y")}#
                        WHERE
                            vinculo = '{dado.vinculo}'
                        """)
                    conn.commit()
                    flag_encontrou = True
                    break
    browser.quit()