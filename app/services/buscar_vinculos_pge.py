from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd
from app.utils.selenium_utils import send_keys, alert_is_present
data_agora = datetime.now()
date_format = f"%d/%m/%Y"

load_dotenv()

def buscar_rh ():
    conn = pyodbc.connect(os.getenv('STRING_ACCES'))
    cursor = conn.cursor()
    rows = cursor.execute(f"SELECT cpf FROM BuscarVinculos WHERE ok = 'modulacao ok'").fetchall()

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

    for dado in rows:
        browser.execute_script("arguments[0].click();", browser.find_element(By.XPATH, '//*[text()="Consulta Ocorrências"]'))
        send_keys(browser,(By.XPATH,"/html/body/form/center/table/tbody/tr/td[2]/input"),dado.cpf)
        browser.find_element(By.XPATH,"//input[@value='Consultar CPF']").click()
        time.sleep (.3)
        if alert_is_present(browser):
            browser.switch_to.alert.accept()
            cursor.execute(f"""
                UPDATE 
                    BuscarVinculos 
                SET 
                    ok = 'ok - nada'
                WHERE 
                    cpf = '{dado.cpf}'
            """)
            conn.commit()
            continue
        select_vinculo = Select(wait.until(EC.presence_of_element_located((By.NAME, "codVinculo"))))
        for option in select_vinculo.options:
            vinculo = option.get_attribute("value")
            if vinculo == '':
                continue
            data_inicio = datetime.strptime(option.text[:10], "%d/%m/%Y").strftime("%Y-%m-%d")

            # Inserção formatada corretamente
            cursor.execute(f"""
                INSERT INTO 
                    ResultadoBuscarVinculos (cpf, vinculo, data_inicio) 
                VALUES 
                    ('{dado.cpf}', '{vinculo}', '{data_inicio}')
                """)
        cursor.execute(f"""
            UPDATE 
                BuscarVinculos 
            SET 
                ok = 'ok'
            WHERE 
                cpf = '{dado.cpf}'
            """)
        conn.commit()
            
    browser.quit()