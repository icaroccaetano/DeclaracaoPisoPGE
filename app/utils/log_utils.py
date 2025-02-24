# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
import os
import traceback

# Imports de terceiros
from flask import session

# Imports locais
from app.config.requests import requests_session

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def registrar_log(tipo: str, mensagem: str):
    """
    Registra um log.

    Args:
        tipo (str): Tipo do log. Exemplo: info, error.
        mensagem (str): Mensagem do log.
    """

    requests_session.post(f'{os.getenv("API_BASE_URL")}/api/crud/Log', 
                            json={"usuario_id": session["usuario"]["id"] if session.get("usuario") else None, 
                                "sistema_id": session["sistema_atual"]["id"] if session.get("sistema_atual") else None, 
                                "tipo": tipo,
                                "mensagem": mensagem})
