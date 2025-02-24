# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
from datetime import datetime
from unicodedata import normalize
import re

# Imports de terceiros

# Imports locais

# =================================================================================================================================================================
# Constantes
# =================================================================================================================================================================

mes_para_numero = {
    "JANEIRO": 1,
    "FEVEREIRO": 2,
    "MARÇO": 3,
    "ABRIL": 4,
    "MAIO": 5,
    "JUNHO": 6,
    "JULHO": 7,
    "AGOSTO": 8,
    "SETEMBRO": 9,
    "OUTUBRO": 10,
    "NOVEMBRO": 11,
    "DEZEMBRO": 12
}

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================


def formatar_cpf(cpf: str) -> str:
    """
    Formata o CPF para o padrão 999.999.999-99.

    Args:
        cpf (str): CPF a ser formatado.

    Returns:
        str: CPF formatado.
    """

    # Remove todos os caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Preenche o CPF com zeros à esquerda até ter 11 dígitos
    cpf = cpf.zfill(11)
    
    # Formata o CPF no padrão 999.999.999-99
    cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
    
    # Retorna o CPF formatado
    return cpf


def formatar_em_timestamp(data: str, hora: str) -> datetime:
    """
    Formata a data e hora em um objeto datetime.

    Args:
        data (str): Data no formato dd/mm/aaaa.
        hora (str): Hora no formato hh:mm.

    Returns:
        datetime: Objeto datetime com a data e hora formatadas.
    
    Raises:
        ValueError: Se a data ou hora estiverem mal formatadas.
    """
    
    # Tenta formatar a data e hora em um objeto datetime
    try:
        data = datetime.strptime(f'{data} {hora}', '%d/%m/%Y %H:%M')
        return data
    except ValueError:
        return None
    

def formatar_nome_sistema(nome: str):
    """
    Remove os caracteres especiais, troca espaços por underline e coloca as letras minúsculas e adiciona sistema.

    Exemplo:
        "Banco de Dados" -> "sistema_de_atualizacao_do_banco"
        "Férias" -> "sistema_ferias"

    Args:
        nome (str): Nome a ser formatado.

    Returns:
        str: Nome formatado.
    """

   # Separa acentos dos caracteres
    nome = normalize('NFKD', nome)

    # Remove acentos, mantendo apenas caracteres ASCII
    nome = nome.encode('ascii', errors='ignore').decode('utf-8')

    # Substitui espaços por underlines
    nome = nome.replace(' ', '_')

    # Remove outros caracteres especiais (mantém letras, números e underlines)
    nome = re.sub(r'[^\w\s]', '', nome)

    # Coloca tudo em minúsculas
    nome = nome.lower()

    return nome


def remover_caracteres_especiais(nome: str):
    """
    Remove os caracteres especiais e coloca as letras minúsculas e adiciona sistema.

    Exemplo:
        "Férias" -> "Ferias"

    Args:
        nome (str): Nome a ser formatado.

    Returns:
        str: Nome formatado.
    """

   # Separa acentos dos caracteres
    nome = normalize('NFKD', nome)

    # Remove acentos, mantendo apenas caracteres ASCII
    nome = nome.encode('ascii', errors='ignore').decode('utf-8')

    # Remove outros caracteres especiais (mantém letras, números e underlines)
    nome = re.sub(r'[^\w\s]', '', nome)

    return nome
