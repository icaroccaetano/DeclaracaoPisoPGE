from app.utils.selenium_utils import iniciar_chrome, find, click, send_keys, clear, switch_to_frame, select_option
from app.database.sql_server_engine import get_sql_server_engine
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyodbc
import pandas as pd
import os
import json
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

def criar_declaracao ():
    # Dados necessarios:
    # - Nome
    # - CPF
    # - Funcao
    # - Desc funcao
    # - Periodo (mm/yyyy a mm/yyyy)
    
    # Criar 1 a 1: -> Selecionar os que estão prontos pra criar
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
            ok = 'ok - 2022'
        AND
            rodou = FALSE
        """).fetchall()
    for servidor in ListaCriar:
        # sql_server_engine = get_sql_server_engine()
        # DadosServidor = pd.read_sql(f"""
        #     SELECT 
        #         * 
        #     FROM 
        #         SGDP_SISTEMA_DE_DECLARACOES_LEVANTAMENTO_PGE_EQUIPARACAO_DE_PISO
        #     WHERE
        #         cpf = '{servidor.cpf}'
        #         """, sql_server_engine)
        DadosServidor = cursor.execute(f"""
            SELECT 
                * 
            FROM 
                TabelaBuscaModulacaoManual
            WHERE
                cpf = '{servidor.cpf}'
                """).fetchall()
        nome_servidor = servidor.nome
        cpf = servidor.cpf
        if not DadosServidor:
            cursor.execute(f"""
                UPDATE 
                    BuscarVinculos 
                SET 
                    ok = 'servidor nao encontrado no levantamento'
                WHERE 
                    cpf = '{servidor.cpf}'
                AND
                    sei = '{servidor.sei}'
                """)
            conn.commit()
            continue
        funcao_servidor = DadosServidor[0][1]   
        descricao_funcao = DadosServidor[0][2]
        # Criar string dos períodos
        ListaPeriodos = cursor.execute(f"""
            SELECT 
                data_inicio,
                data_fim
            FROM 
                ResultadoBuscarVinculos 
            WHERE 
                cpf = '{cpf}'
            """).fetchall()
        periodos_lista = []
        for dados in ListaPeriodos:
            # se a data_inicio for menor que 2016 - considerar
            if dados.data_inicio > datetime.strptime("01/01/2017", "%d/%m/%Y"):
                data_inicio = datetime.strftime(dados.data_inicio, "%m/%Y")
                data_fim = datetime.strftime(dados.data_fim, "%m/%Y")
                periodos_lista.append(f"{data_inicio} a {data_fim}")
        periodos = ", ".join(periodos_lista) + "."
        # Criacao do HTML
        html = ""  
        html = html + f"<br><br><br><br>"
        html = html + f"""
        <p style='margin-left:  100px;'>Declaramos, para os fins do art. 2º, III da Resolução nº 2/2024-PGE/CCMA, 
        que {nome_servidor}, CPF {cpf}, exerceu a função nº {str(funcao_servidor)} ({descricao_funcao}), 
        que É considerada função de magistério, conforme disciplina o art. 2º, §2º da Lei nº 11.738/2008, no período {periodos}</p><br>"""
        html = html + f"""
        <p style='margin-left:  100px;'><b>Goiânia, data da assinatura eletrônica.</b></p>
        <p style="text-align: center;"><b>HUDSON AMARAU DE OLIVEIRA</b></p>
        <p style="text-align: center;">Superintendente de Gestão e Desenvolvimento de Pessoas</p>
        """
        if descricao_funcao == "COORDENADOR DO PROGRAMA DO ENSINO MÉDIO INOVADOR -":
            html = html.replace("que É considerada", "que NÃO É considerada")
        html = json.dumps(html)

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
        browser.execute_script("arguments[0].click()", browser.find_element(By.XPATH, "//*[text()='SEDUC/SGDP-15916']"))
        clear(browser,(By.ID, 'txtPesquisaRapida'))
        send_keys(browser, (By.ID, 'txtPesquisaRapida'), servidor.sei)
        browser.execute_script("document.getElementById('frmProtocoloPesquisaRapida').submit();")
        browser.switch_to.frame("ifrVisualizacao")
        #click(browser,(By.CSS_SELECTOR, "[title='Reabrir Processo']"))
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title='Incluir Documento']")))
        click(browser,(By.CSS_SELECTOR, "[title='Incluir Documento']"))
        click(browser,(By.XPATH, "//*[text()='Declaração']"))
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, "txtNomeArvore")))
        send_keys(browser, (By.ID, "txtNomeArvore"),"Declaracão para Equiparação de Piso")
        click(browser,(By.ID, "lblRestrito"))
        select_element = browser.find_element(By.ID, "selHipoteseLegal")
        for option in select_element.find_elements(By.TAG_NAME, 'option'):
            if option.text == "Outras Hipóteses (Art. 55, III da Instrução Normativa nº 008/2017)":
                option.click()
                break
        click(browser,(By.ID, "btnSalvar"))

        # Aguarda até que uma nova janela seja detectada
        while len(browser.window_handles) == 1:
            time.sleep(2) 
        browser.switch_to.window(browser.window_handles[-1])

        #WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title='ementa']")))
        
        iframe = browser.find_element(By.CSS_SELECTOR, "[title='Corpo do Texto']")
        browser.switch_to.frame(iframe)
        browser.execute_script(f"document.body.innerHTML = {html};")
        time.sleep(1)
        browser.switch_to.default_content()
        
        iframe = browser.find_element(By.CSS_SELECTOR, "[title='Data']")
        browser.switch_to.frame(iframe)
        browser.execute_script("document.body.innerHTML = '';")
        time.sleep(1)
        browser.switch_to.default_content()
        
        while browser.find_element(By.CSS_SELECTOR, "[title='Salvar (Ctrl+Alt+S)']").get_attribute("aria-disabled") == "false":
            browser.execute_script("arguments[0].click();", browser.find_element(By.CSS_SELECTOR, "[title='Salvar (Ctrl+Alt+S)']"))
            time.sleep(5)

        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        browser.switch_to.default_content()
        browser.switch_to.frame("ifrVisualizacao")
        browser.execute_script("arguments[0].click()", browser.find_element(By.CSS_SELECTOR, "[title='Assinar Documento']"))
        browser.switch_to.default_content()
        iframe = browser.find_element(By.NAME, "modal-frame")
        browser.switch_to.frame(iframe)
        selecionador = browser.find_element(By.ID, "selCargoFuncao")
        options = selecionador.find_elements(By.TAG_NAME, "option")
        for opt in options:
            if opt.text == "Superintendente":
                opt.click()
                break
        senha_input = browser.find_element(By.ID, "pwdSenha")
        senha_input.click()
        senha_input.clear()
        senha_input.send_keys(os.getenv('SENHA_SEI'))  # Certifique-se de que a variável SENHA está definida
        browser.execute_script("assinarSenha();")

        cursor.execute(f"""
            UPDATE 
                BuscarVinculos 
            SET 
                rodou = TRUE
            WHERE 
                cpf = '{servidor.cpf}'
            AND
                sei = '{servidor.sei}'
            """)
        conn.commit()
        browser.switch_to.default_content()
        browser.switch_to.frame("ifrVisualizacao")
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[title='Incluir Documento']")))
        browser.close()
