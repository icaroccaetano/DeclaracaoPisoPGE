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
from selenium.common import exceptions

# Imports locais
from app.config.socketio import socketio
from app.utils.selenium_utils import send_keys, click, clear

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def realizar_login(driver: webdriver, exception: bool = True, socket: bool = True) -> bool:
    """
    Realiza o login no sistema Goiás 360.

    Args:
        driver (WebDriver): Instância do WebDriver.
        exception (bool): Se True, lança exceção em caso de erro.
        socket (bool): Se True, envia mensagens de erro para o frontend.

    Returns:
        bool: True se o login foi realizado com sucesso, False caso contrário.

    Raises:
        Exception: Se ocorrer um erro ao realizar o login.
    """

    # Acessa a página de login
    driver.get("https://goias360.educacao.go.gov.br/Login.html")

    # Envia o usuário
    clear(driver, (By.ID, "usuario"))
    send_keys(driver, (By.ID, "usuario"), os.getenv("usuario_Goias360"))

    # Envia a senha
    clear(driver, (By.ID, "senha"))
    send_keys(driver, (By.ID, "senha"), os.getenv("senha_Goias360"))

    # Clica no botão de login
    click(driver, (By.XPATH, '//*[@id="login"]/div[1]/div[3]/div/div[2]/div/div[3]/div/input'))

    # Verifica se o login foi realizado com sucesso
    try:
        WebDriverWait(driver, 5).until(EC.any_of(
            EC.presence_of_element_located((By.CLASS_NAME, 'icone-educacao360')), 
            EC.presence_of_element_located((By.XPATH, '//*[text()="Usuário não autorizado!"]')),
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"The user name or password is incorrect.")]'))))
    
    # Tempo de espera da verificação excedido
    except exceptions.TimeoutException:

        # Clica novamente no botão de login caso o clique não tenha sido corretamente registrado
        click(driver, (By.XPATH, '//*[@id="login"]/div[1]/div[3]/div/div[2]/div/div[3]/div/input'))

        # Verifica se o login foi realizado com sucesso
        WebDriverWait(driver, 5).until(EC.any_of(
            EC.presence_of_element_located((By.CLASS_NAME, 'icone-educacao360')), 
            EC.presence_of_element_located((By.XPATH, '//*[text()="Usuário não autorizado!"]')),
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"The user name or password is incorrect.")]'))))

    # Verifica se o login foi realizado com sucesso
    if len(driver.find_elements(By.CLASS_NAME, 'icone-educacao360')) == 1:

        # Retorna True em caso de sucesso
        return True
    
    # Envia mensagem de erro para o frontend de acordo com a flag socket
    if socket:
        socketio.emit('login_error', {'sistema': 'Goias360', 'message': 'Tempo de espera excedido.'})

    # Registra o erro de acordo com a flag exception
    if exception:
        raise Exception("Tempo de espera excedido.")
        
    # Retorna False em caso de erro
    return False