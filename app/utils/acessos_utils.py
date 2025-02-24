# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
from functools import wraps
import logging
import os
import traceback

# Imports de terceiros
from flask import flash, redirect, session, url_for

# Imports locais
from app.config.requests import requests_session
from app.utils.encode_utils import encode_string

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================


def login_requerido():
    """
    Decorator para verificar se o usuário está logado.

    Returns:
        function: Função decorada.
    """

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            # Verifica se o usuário está logado
            if not session.get("jwt") or not session.get("usuario") or not session.get("servidor"):
                flash("Faça login para acessar a página.", "error")
                return redirect(url_for('login_page.login'))

            # Atualiza o token de autenticação no header
            requests_session.headers.update({"Authorization": f'Bearer {session["jwt"]}'})

            return f(*args, **kwargs)

        return decorated_function
    
    return decorator


def is_authenticated():
    """
    Verifica se o usuário está autenticado.

    Returns:
        bool: True se o usuário estiver autenticado, False caso contrário.
    """

    # Verifica se o usuário está logado
    if not session.get("jwt") or not session.get("usuario") or not session.get("servidor") or not session.get("acessos"):
        return False

    return True


def acesso_requerido(sistema: str, descricao_nivel_minimo: str):
    """
    Decorator para verificar se o usuário possui acesso ao sistema.

    Args:
        sistema (str): Nome do sistema.
        descricao_nivel_minimo (str): Nível de acesso mínimo.
    
    Returns:
        function: Função decorada.
    """

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            # Busca o nível de acesso mínimo no banco de dados
            try:
                response = requests_session.post(f'{os.getenv("API_BASE_URL")}/api/sistema_de_acessos/nivel_acesso_by_descricao', json={"descricao": descricao_nivel_minimo})
                nivel = response.json()["data"]
            except Exception as e:
                logging.error(f"Erro ao buscar nível de acesso: {e}")
                flash("Erro ao buscar nível de acesso.", "error")
                return redirect(url_for('home_page.home'))

            # Verifica se o nível de acesso mínimo foi encontrado
            if not nivel:
                flash(f"Nível de acesso não encontrado: {descricao_nivel_minimo}.", "error")
                return redirect(url_for('home_page.home'))

            # Verifica se o usuário possui permissões suficientes para acessar o sistema
            for acesso in session["acessos"]:
                if acesso["sistema"]["nome"] == sistema and acesso["nivel_acesso_id"] >= nivel["id"]:

                    # Seta o sistema que o usuário está acessando na sessão
                    session["sistema_atual"] = acesso["sistema"]
                    session["nivel_acesso_atual"] = acesso["nivel_acesso"]

                    # Retorna a função decorada
                    return f(*args, **kwargs)

            # Mensagem de erro
            flash(f"Usuário não possui os acessos necessários para acessar o sistema: {sistema} - {nivel["descricao"]}.", "error")
            return redirect(url_for('home_page.home'))

        return decorated_function
    
    return decorator


def get_nivel_acesso_usuario(sistema: str) -> int:
    """
    Retorna o nível de acesso do usuário em um sistema.

    Args:
        sistema (str): Nome do sistema a ser pesquisado.

    Returns:
        int: Nível de acesso do usuário ou 0 caso não encontre.
    """

    # Busca o nível de acesso do usuário
    for acesso in session["acessos"]:
        if acesso["sistema"]["nome"] == sistema:
            return acesso["nivel_acesso"]["nivel"]
        
    # Retorna 0 caso não encontre o nível de acesso
    return 0


def save_user_data():
    """
    Salva os dados de um usuário em um arquivo codificado.
    """

    # Chaves específicas a serem salvas
    keys = ["Expresso", "Goias360", "Modulacao", "SEI"]

    # Filtra as chaves
    encoded_content = ""
    for key in keys:
        if "usuario_" + key in os.environ:
            encoded_content = encoded_content + (f"usuario_{key}={os.getenv('usuario_Expresso')}\n")
            encoded_content = encoded_content + (f"senha_{key}={os.getenv('senha_Expresso')}\n")

    # Codfica o conteúdo
    encoded_content = encode_string(encoded_content, "tmp/.user")