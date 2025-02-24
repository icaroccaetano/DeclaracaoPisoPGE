# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
import time
import logging
import traceback

# Imports de terceiros
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

# Imports locais

# =================================================================================================================================================================
# Constantes
# =================================================================================================================================================================



# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def iniciar_chrome(download_path: str = None, headless: bool = False, implicit_wait: float = 3) -> webdriver.Chrome:
    """
    Inicia o WebDriver.

    Args:
        download_path (str): Caminho onde os arquivos serão baixados.
        headless (bool): Indica se o navegador será iniciado em modo headless.
        implicit_wait (float): Tempo de espera implícito para localizar elementos.

    Returns:
        WebDriver: Instância do WebDriver configurado.
    """

    # Configura as opções do WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") # Inicia o navegador maximizado

    # Configura o WebDriver para iniciar em modo headless
    if headless:
        options.add_argument("--headless")
    
    # Configura as opções de download do WebDriver
    if download_path:
        options.add_experimental_option('prefs', {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })

    # Inicia o WebDriver
    driver = webdriver.Chrome(options=options)

    # Configura o tempo de espera implícito
    driver.implicitly_wait(implicit_wait)

    # Retorna o WebDriver configurado
    return driver


def iniciar_firefox(download_path: str = None, headless: bool = False, implicit_wait: float = 3) -> webdriver.Firefox:
    """
    Inicia o WebDriver.

    Args:
        download_path (str): Caminho onde os arquivos serão baixados.
        headless (bool): Indica se o navegador será iniciado em modo headless.
        implicit_wait (float): Tempo de espera implícito para localizar elementos.

    Returns:
        WebDriver: Instância do WebDriver configurado.
    """

    # Configura as opções do WebDriver
    options = webdriver.FirefoxOptions()

    # Configura o WebDriver para iniciar em modo headless
    if headless:
        options.add_argument("--headless")
    
    # Configura as opções de download do WebDriver
    if download_path:
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_path)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

    # Inicia o WebDriver
    driver = webdriver.Firefox(options=options)

    # Maximiza a janela
    driver.maximize_window()

    # Configura o tempo de espera implícito
    driver.implicitly_wait(implicit_wait)

    # Retorna o WebDriver configurado
    return driver


def alert_is_present(driver: webdriver) -> bool:
    """
    Verifica se um alerta está presente na página.

    Args:
        driver (WebDriver): Instância do WebDriver.

    Returns:
        bool: Indica se um alerta está presente.
    """

    try:
        
        # Tenta acessar o alerta. Se não existir, uma exceção será lançada
        driver.switch_to.alert

        # Retorna True se o alerta estiver presente
        return True
    
    except:

        # Retorna False se o alerta não estiver presente
        return False
    

def find(driver: webdriver, locator: tuple, text: str = None, exact_match: bool = False, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> WebElement:
    """
    Busca um elemento na página.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do elemento.
        text (str): Busca o elemento pelo texto, se fornecido.
        exact_match (bool): Indica se a comparação do texto deve ser exata.
        retries (int): Número de tentativas para clicar no elemento.
        delay (int): Tempo de espera entre as tentativas.
        exception (bool): Indica se uma exceção deve ser lançada em caso de erro.
        verbose (bool): Indica se mensagens de log devem ser exibidas.

    Returns:
        WebElement: Elemento encontrado.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca o elemento
            if text:
                element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]" if not exact_match else f"//*[text()='{text}']")
            else:
                element = driver.find_element(*locator)

            # Retorna o elemento se ele foi encontrado
            return element
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível clicar no elemento {locator or text} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna None se o elemento não foi encontrado
                return None
            

def click(driver: webdriver, locator: tuple, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> bool:
    """
    Clica em um elemento da página.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do elemento.
        retries (int): Número de tentativas para clicar no elemento.
        delay (int): Tempo de espera entre as tentativas.
        exception (bool): Indica se uma exceção deve ser lançada em caso de erro.
        verbose (bool): Indica se mensagens de log devem ser exibidas.

    Returns:
        bool: Indica se o elemento foi clicado com sucesso.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca o elemento
            element = driver.find_element(*locator)

            # Clica no elemento
            element.click()

            # Retorna True se o elemento foi clicado com sucesso
            return True
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível clicar no elemento {locator} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna False se o elemento não foi clicado com sucesso
                return False


def click_on_invisible_element(driver: webdriver, locator: tuple, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> bool:
    """
    Clica em um elemento da página que possui display: none.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do elemento.
        retries (int): Número de tentativas para clicar no elemento.
        delay (int): Tempo de espera entre as tentativas.
        exception (bool): Indica se uma exceção deve ser lançada em caso de erro.
        verbose (bool): Indica se mensagens de log devem ser exibidas.

    Returns:
        bool: Indica se o elemento foi clicado com sucesso.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca o elemento
            element = driver.find_element(*locator)

            # Clica no elemento
            driver.execute_script("arguments[0].click();", element)

            # Retorna True se o elemento foi clicado com sucesso
            return True
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível clicar no elemento {locator} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna False se o elemento não foi clicado com sucesso
                return False
    

def send_keys(driver: webdriver, locator: tuple, keys: str, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> bool:
    """
    Insere texto em um campo de texto.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do elemento.
        keys (str): Texto a ser inserido no campo.
        retries (int): Número de tentativas para inserir o texto.
        delay (int): Tempo de espera entre as tentativas.
        verbose (bool): Indica se mensagens de log devem ser exibidas.

    Returns:
        bool: Indica se o texto foi inserido com sucesso.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca o elemento
            element = driver.find_element(*locator)

            # Limpa o campo antes de inserir o texto
            element.clear()

            # Insere o texto no campo
            element.send_keys(keys)

            # Verifica se o texto foi inserido corretamente
            if element.get_attribute("value") == keys:
                    
                # Retorna True se o texto foi inserido com sucesso
                return True
            
            raise Exception("Texto não inserido corretamente")
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível inserir texto no campo {locator} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna False se o texto não foi inserido com sucesso
                return False


def clear(driver: webdriver, locator: tuple, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> bool:
    """
    Limpa um campo de texto.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do elemento.
        retries (int): Número de tentativas para limpar o campo.
        delay (int): Tempo de espera entre as tentativas.
        exception (bool): Indica se uma exceção deve ser lançada em caso de erro.
        verbose (bool): Indica se mensagens de log devem ser exibidas.

    Returns:
        bool: Indica se o campo foi limpo com sucesso.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca o elemento
            element = driver.find_element(*locator)

            # Limpa o campo
            element.clear()

            # Retorna True se o campo foi limpo com sucesso
            return True
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível limpar o campo {locator} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna False se o campo não foi limpo com sucesso
                return False
            

def wait_for_staleness_or_timeout(driver: webdriver, locator: tuple = None, element: WebElement = None, timeout: float = 2) -> None:
    """
    Aguarda até que um elemento fique obsoleto.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do elemento. Se fornecido, o elemento será buscado.
        element (WebElement): Elemento a ser verificado. Se fornecido, o localizador será ignorado.
        timeout (float): Tempo máximo de espera em segundos.
    """

    try:

        # Se o elemento não for fornecido, busca o elemento pelo localizador
        if not element:
                
            # Busca o elemento
            element = driver.find_element(*locator)

        # Aguarda até que o elemento fique obsoleto
        WebDriverWait(driver, timeout).until(EC.staleness_of(element))


    # Ignora exceções de tempo limite
    except exceptions.TimeoutException:
        pass


def get_table_data(driver: webdriver, locator: tuple, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> list:
    """
    Extrai dados de uma tabela.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador da tabela.

    Returns:
        list: Lista de linhas da tabela contendo uma lista de células.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca a tabela
            table = driver.find_element(*locator)

            # Extrai os dados da tabela
            table_data = [[cell.text for cell in row.find_elements(By.TAG_NAME, "td")] for row in table.find_elements(By.TAG_NAME, "tr")]

            # Retorna os dados da tabela
            return table_data
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível extrair os dados da tabela {locator} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna uma lista vazia se os dados da tabela não foram extraídos com sucesso
                return []
        

def switch_to_frame(driver: webdriver, locator: tuple, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> bool:
    """
    Alterna o foco para um frame.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do frame.
        retries (int): Número de tentativas para alternar o foco.
        delay (int): Tempo de espera entre as tentativas.
        exception (bool): Indica se uma exceção deve ser lançada em caso de erro.
        verbose (bool): Indica se mensagens de log devem ser exibidas.

    Returns:
        bool: Indica se o foco foi alterado com sucesso.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca o frame
            frame = driver.find_element(*locator)

            # Alterna o foco para o frame
            driver.switch_to.frame(frame)

            # Retorna True se o foco foi alterado com sucesso
            return True
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível alternar o foco para o frame {locator} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna False se o foco não foi alterado com sucesso
                return False
            

def select_option(driver: webdriver, locator: tuple, option_text: str = None, option_value: str = None, retries: int = 5, delay: float = 0.25, exception: bool = True, verbose: bool = True) -> bool:
    """
    Seleciona uma opção em um campo select.

    Args:
        driver (WebDriver): Instância do WebDriver.
        locator (tuple): Localizador do campo select.
        option_text (str): Texto da opção a ser selecionada.
        option_value (str): Valor da opção a ser selecionada. Se fornecido, o texto da opção será ignorado.
        retries (int): Número de tentativas para selecionar a opção.
        delay (int): Tempo de espera entre as tentativas.
        exception (bool): Indica se uma exceção deve ser lançada em caso de erro.
        verbose (bool): Indica se mensagens de log devem ser exibidas.

    Returns:
        bool: Indica se a opção foi selecionada com sucesso.
    """

    # Inicia o contador de tentativas
    attempts = 0

    # Realiza as tentativas
    while attempts < retries:

        try:

            # Busca o campo select
            select = driver.find_element(*locator)
            
            # Seleciona a opção pelo value
            if option_value:
                select.find_element(By.CSS_SELECTOR, f"option[value='{option_value}']").click()

            # Seleciona a opção pelo texto
            else:
                select.find_element(By.XPATH, f"//*[contains(text(),'{option_text}')]").click()

            # Retorna True se a opção foi selecionada com sucesso
            return True
        
        except Exception as e:

            # Incrementa o contador de tentativas
            attempts += 1

            # Aguarda o tempo de delay antes de tentar novamente
            time.sleep(delay)

            # Verifica se o número de tentativas foi excedido
            if attempts == retries:

                # Loga o erro
                if verbose:
                    logging.error(f"Não foi possível selecionar a opção {option_text or option_value} no campo select {locator} após {retries} tentativas: " + str(e) + "\n" + traceback.format_exc())

                # Lança uma exceção se a flag exception estiver ativada
                if exception:
                    raise

                # Retorna False se a opção não foi selecionada com sucesso
                return False