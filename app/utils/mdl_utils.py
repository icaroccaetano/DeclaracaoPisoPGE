# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
import os

# Imports de terceiros
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Imports locais
from app.config.socketio import socketio
from app.utils.selenium_utils import send_keys, click, clear


# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================


def realizar_login(driver: webdriver, exception: bool = True, socket: bool = True) -> bool:
    """
    Realiza o login no sistema MDL (Modulação) usando as credenciais fornecidas.

    Args:
        driver (webdriver): Instância do WebDriver.
        socket (bool): Se True, envia mensagens de erro para o frontend.

    Returns:
        bool: True se o login foi realizado com sucesso, False caso contrário.

    Raises:
        Exception: Se ocorrer um erro ao realizar o login.
    """
    
    # Acessa a página de login
    driver.get("https://modulacao.educacao.go.gov.br")

    # Envia o usuário
    clear(driver, (By.ID, "txtLogin"))
    send_keys(driver, (By.ID, "txtLogin"), os.getenv("usuario_Modulacao"))

    # Envia a senha
    clear(driver, (By.ID, "txtSenha"))
    send_keys(driver, (By.ID, "txtSenha"), os.getenv("senha_Modulacao"))

    # Clica no botão de login
    driver.find_element(By.ID, 'btnLogon').click()

    # Verifica se o login foi realizado com sucesso. A modulação não mostra indicador de usuário/senha inválidos
    try:
        driver.find_element(By.XPATH, '//*[text()="Consultar Modulação Servidor"]')
        return True
    
    # Se não encontrou o elemento, o login falhou
    except:

        # Envia mensagem de erro para o frontend de acordo com a flag socket
        if socket:
            socketio.emit('login_error', {'sistema': 'Modulacao', 'message': 'Tempo de espera excedido.'})

        # Se o login falhou, lança exceção
        if exception:
            raise Exception("Erro ao realizar login no sistema Expresso.")
        
        # Retorna False se o login falhou
        return False