# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
import multiprocessing
import threading
from functools import partial

# Imports de terceiros

# Imports locais

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def _split_list_into_chunks(list, num_chunks):
    """
    Divide a lista no número de pedaços especificado.

    Args:
        list (list): Lista a ser dividida.
        num_chunks (int): Número de pedaços.

    Returns:
        list: Lista de listas divididas.

    Exemplo:
    _split_list_into_chunks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3) -> [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]
    """

    # Calcula o tamanho dos pedaços
    chunk_size = len(list) // num_chunks
    remainder = len(list) % num_chunks

    # Divide a lista no número de pedaços especificado
    chunks = []
    start = 0
    for i in range(num_chunks):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(list[start:end])
        start = end

    # Retorna os pedaços
    return chunks


def criar_threads(func, list, num_threads, args=None):
    """
    Divide a lista em grupos e executa a função em paralelo em cada grupo.

    Args:
        func (function): Função a ser executada em paralelo.
        list (list): Lista a ser dividida em grupos.
        num_threads (int): Número de threads a serem criadas.

    Returns:
        list: Lista processada.
    """

    # Divide a lista em grupos a serem processados por cada thread
    grupos = _split_list_into_chunks(list, num_threads)

    # Define a função parcial com os parâmetros fixos para facilitar o mapeamento de processos
    func = partial(func, **args)

    # Cria as threads
    threads = []
    for grupo in grupos:
        t = threading.Thread(target=func, args=(grupo,))
        threads.append(t)
        t.start()

    # Espera as threads terminarem
    for t in threads:
        t.join()

    # Junta os grupos
    list = []
    for grupo in grupos:
        list.extend(grupo)

    # Retorna a lista processada
    return list


def criar_processos(func: callable, lista: list, num_processos: int, args: dict = None):
    """
    Divide a lista em grupos e executa a função em paralelo em cada grupo usando processos.

    Args:
        func (function): Função a ser executada em paralelo.
        lista (list): Lista a ser dividida em grupos.
        num_processos (int): Número de processos a serem criados.
        args (dict): Dicionário de argumentos a serem passados para a função.

    Returns:
        list: Lista processada.
    """

    # Divide a lista em grupos a serem processados por cada processo
    grupos = _split_list_into_chunks(lista, num_processos)

    # Define a função parcial com os parâmetros fixos para facilitar o mapeamento de processos
    func = partial(func, **args)

    # Cria um pool de processos
    with multiprocessing.Pool(processes=num_processos) as pool:
        resultados = pool.map(func, grupos)

    # Junta os grupos processados
    lista_processada = []
    for resultado in resultados:
        lista_processada.extend(resultado)

    # Retorna a lista processada
    return lista_processada