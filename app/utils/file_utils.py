# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
import os
import logging
import zipfile

# Imports de terceiros

# Imports locais

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def remover(filepath: str) -> bool:
    """
    Remove um arquivo do sistema.

    Args:
        filepath (str): Caminho do arquivo a ser removido.

    Returns:
        bool: Indica se o arquivo foi removido com sucesso.
    """

    try:
        logging.info(f"Removendo arquivo {filepath}.")
        os.remove(filepath)
        logging.info(f"Arquivo {filepath} removido com sucesso.")
        return True
    except FileNotFoundError:
        logging.error(f"Arquivo {filepath} não encontrado.")
        return False
    except PermissionError:
        logging.error(f"Permissão negada para remover o arquivo {filepath}.")
        return False
    except Exception as e:
        logging.error(f"Erro ao remover o arquivo {filepath}: {e}")
        return False
    

def unzipar(filepath: str, extract_path: str) -> bool:
    """
    Extrai um arquivo zipado.

    Args:
        filepath (str): Caminho do arquivo zipado.
        extract_path (str): Caminho onde o arquivo será extraído.

    Returns:
        bool: Indica se o arquivo foi extraído com sucesso.
    """

    try:
        logging.info(f"Extraindo arquivo {filepath}.")
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        logging.info(f"Arquivo {filepath} extraído com sucesso.")
        return True
    
    except FileNotFoundError:
        logging.error(f"Arquivo {filepath} não encontrado.")
        return False
    
    except PermissionError:
        logging.error(f"Permissão negada para extrair o arquivo {filepath}.")
        return False
    
    except Exception as e:
        logging.error(f"Erro ao extrair o arquivo {filepath}: {e}")
        return False