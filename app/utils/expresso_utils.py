# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões


# Imports de terceiros
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Imports locais
from app.config.socketio import socketio
from app.utils.selenium_utils import click, send_keys, clear

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def realizar_login(driver: webdriver, exception: bool = True, socket: bool = True) -> bool:
    """
    Realiza o login no sistema Expresso.

    Args:
        driver (WebDriver): Instância do WebDriver.
        exception (bool): Se True, lança exceção em caso de erro.
        socket (bool): Se True, envia mensagens de erro para o frontend.

    Returns:
        bool: Indica se o login foi realizado com sucesso.
    """

    # Acessa a página de login
    driver.get("https://aplicacoes.expresso.go.gov.br/")

    # Envia o usuário
    clear(driver, (By.ID, "usernameUserInput"))
    send_keys(driver, (By.ID, "usernameUserInput"), os.getenv("usuario_Expresso"))

    # Envia a senha
    clear(driver, (By.ID, "password"))
    send_keys(driver, (By.ID, "password"), os.getenv("senha_Expresso"))

    # Clica no botão de login
    click(driver, (By.XPATH, '//*[text()="Continuar"]'))

    # Verifica se o login foi realizado com sucesso
    WebDriverWait(driver, 5).until(EC.any_of(
        EC.presence_of_element_located((By.XPATH, '//*[text()="Login falhou! Favor verifique o usuário e senha e tente novamente."]')),
        EC.presence_of_element_located((By.XPATH, '//*[text()="Sistema de Frequência"]'))))

    # Verifica se o login foi realizado com sucesso
    if len(driver.find_elements(By.XPATH, '//*[text()="Sistema de Frequência"]')) == 1:

        # Retorna True se o login foi realizado com sucesso
        return True
    
    # Envia mensagem de erro para o frontend de acordo com a flag socket
    if socket:
        socketio.emit('login_error', {'sistema': 'Expresso', 'message': 'Tempo de espera excedido.'})

    # Se o login falhou, lança exceção
    if exception:
        raise Exception("Erro ao realizar login no sistema Expresso.")
    
    # Retorna False se o login falhou
    return False


def realizar_login_with_credentials(driver: webdriver, username: str, senha: str, exception: bool = True, socket: bool = True) -> bool:
    """
    Realiza o login no sistema Expresso com as credenciais fornecidas. Necessário quando trabalhando com processos fora do contexto do Flask.

    Args:
        driver (WebDriver): Instância do WebDriver.
        username (str): Nome de usuário.
        senha (str): Senha do usuário.
        exception (bool): Se True, lança exceção em caso de erro.
        socket (bool): Se True, envia mensagens de erro para o frontend.

    Returns:
        bool: Indica se o login foi realizado com sucesso.
    """

    # Acessa a página de login
    driver.get("https://aplicacoes.expresso.go.gov.br/")

    # Envia o usuário
    clear(driver, (By.ID, "usernameUserInput"))
    send_keys(driver, (By.ID, "usernameUserInput"), username)

    # Envia a senha
    clear(driver, (By.ID, "password"))
    send_keys(driver, (By.ID, "password"), senha)

    # Clica no botão de login
    click(driver, (By.XPATH, '//*[text()="Continuar"]'))

    # Verifica se o login foi realizado com sucesso
    WebDriverWait(driver, 5).until(EC.any_of(
        EC.presence_of_element_located((By.XPATH, '//*[text()="Login falhou! Favor verifique o usuário e senha e tente novamente."]')),
        EC.presence_of_element_located((By.XPATH, '//*[text()="Sistema de Frequência"]'))))

    # Verifica se o login foi realizado com sucesso
    if len(driver.find_elements(By.XPATH, '//*[text()="Sistema de Frequência"]')) == 1:

        # Retorna True se o login foi realizado com sucesso
        return True
    
    # Envia mensagem de erro para o frontend de acordo com a flag socket
    if socket:
        socketio.emit('login_error', {'sistema': 'Expresso', 'message': 'Tempo de espera excedido.'})

    # Se o login falhou, lança exceção
    if exception:
        raise Exception("Erro ao realizar login no sistema Expresso.")
    
    # Retorna False se o login falhou
    return False