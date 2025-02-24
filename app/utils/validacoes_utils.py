# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
from datetime import datetime

# Imports de terceiros

# Imports locais

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def validar_data(data: str) -> bool:
    """
    Valida a data no formato dd/mm/aaaa.

    Args:
        data (str): Data a ser validada.

    Returns:
        bool: True se a data estiver no formato correto, False caso contrário.
    """

    try:
        # Tenta converter a string para um objeto datetime no formato dd/mm/aaaa
        datetime.strptime(data, '%d/%m/%Y')
        return True
        
    except ValueError:
        # Se ocorrer um ValueError, a data não está no formato correto
        return False