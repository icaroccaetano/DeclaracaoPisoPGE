from app.utils.selenium_utils import iniciar_chrome, click, send_keys, clear
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def fechar_processos ():
    conn = pyodbc.connect(os.getenv('STRING_ACCES'))
    cursor = conn.cursor()
    ListaCriar = cursor.execute("""
                                SELECT 
                                    cpf, 
                                    nome,
                                    sei
                                FROM 
                                    BuscarVinculos 
                                WHERE 
                                    ok = 'rodar'
                                AND
                                    rodou = TRUE
                                """).fetchall()
    browser = iniciar_chrome() 
    browser.get('https://sei.go.gov.br')
    send_keys(browser, (By.ID, 'txtUsuario'),(os.getenv('ACESSO_SEI')))
    browser.find_element(By.ID, 'pwdSenha').send_keys(os.getenv('SENHA_SEI'))
    select_element = browser.find_element(By.ID, 'selOrgao')
    for option in select_element.find_elements(By.TAG_NAME, 'option'):
        if option.text == 'SEDUC':
            option.click()
            break
    browser.find_element(By.ID, 'Acessar').click() 
    browser.execute_script("arguments[0].click()", browser.find_element(By.ID, 'lnkInfraUnidade'))
    browser.execute_script("arguments[0].click()", browser.find_element(By.XPATH, "//*[text()='SEDUC/GEFOP-11159']"))
    for servidor in ListaCriar:
        browser.switch_to.default_content()
        clear(browser,(By.ID, 'txtPesquisaRapida'))
        send_keys(browser, (By.ID, 'txtPesquisaRapida'), servidor.sei)
        browser.execute_script("document.getElementById('frmProtocoloPesquisaRapida').submit();")
        browser.switch_to.frame("ifrVisualizacao")
        click(browser,(By.CSS_SELECTOR, "[title='Concluir Processo']"))
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title='Reabrir Processo']")))
        cursor.execute(f"""
                    UPDATE 
                        BuscarVinculos 
                    SET 
                        ok = 'enviado e encerrado'
                    WHERE 
                        cpf = '{servidor.cpf}'
                    AND
                        sei = '{servidor.sei}'
                    """)
        conn.commit()
    browser.close()