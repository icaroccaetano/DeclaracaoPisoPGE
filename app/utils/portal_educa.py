# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões

# Imports de terceiros
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Imports locais
from app.utils.selenium_utils import click, send_keys

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================
def realizar_login(driver: webdriver,exception: bool = True, socket: bool = True) -> bool:
    """
    Realiza o login no sistema Portal educa.

    Args:
        driver (WebDriver): Instância do WebDriver.
        exception (bool): Se True, lança exceção em caso de erro.
        socket (bool): Se True, envia mensagens de erro para o frontend.

    Returns:
        bool: Indica se o login foi realizado com sucesso.
    """

    # Acessa a página de login
    driver.get("https://goias.gov.br/educacao/administrator")

    # Insere as credenciaias de login
    send_keys(driver, (By.ID, "user_login"))
    send_keys(driver, (By.ID, "user_pass"))
    
    # Clica no botão submit
    click(driver, (By.ID, 'wp-submit'))