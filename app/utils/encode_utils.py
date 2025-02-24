# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
import base64

# Imports de terceiros

# Imports locais

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def encode(path: str, encoded_path: str) -> None:
    """
    Codifica o conteúdo de um arquivo em base64 e salva em outro arquivo. Utilizado para dificultar a leitura de informações sensíveis.

    Args:
        path (str): Caminho do arquivo a ser codificado.
        encoded_path (str): Caminho do arquivo onde o conteúdo codificado será salvo.
    """

    # Read the values from the file
    with open(path, 'r') as file:
        content = file.read()

    # Encode the content
    encoded_content = base64.b64encode(content.encode('utf-8'))

    # Save the encoded content to a file
    with open(encoded_path, 'wb') as encoded_file:
        encoded_file.write(encoded_content)


def encode_string(content: str, encoded_path: str) -> str:
    """
    Codifica uma string em base64.

    Args:
        content (str): Conteúdo a ser codificado.
        encoded_path (str): Caminho do arquivo onde o conteúdo codificado será salvo.

    Returns:
        str: Conteúdo codificado.
    """

    # Codfica o conteúdo
    encoded_content = base64.b64encode(content.encode('utf-8'))

    # Salva o conteúdo codificado em um arquivo
    with open(encoded_path, 'wb') as encoded_file:
        encoded_file.write(encoded_content)


def decode(path: str):
    """
    Decodifica o conteúdo de um arquivo em base64.

    Args:
        path (str): Caminho do arquivo a ser decodificado.

    Returns:
        str: Conteúdo decodificado.
    """

    # Read the encoded content
    with open(path, 'rb') as encoded_file:
        encoded_content = encoded_file.read()

    # Decode the content
    decoded_content = base64.b64decode(encoded_content).decode('utf-8')

    # Use the decoded content
    return decoded_content
