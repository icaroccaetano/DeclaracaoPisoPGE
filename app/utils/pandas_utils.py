"""As funções desse módulo ainda devem ser simplificadas."""

# =================================================================================================================================================================
# Imports
# =================================================================================================================================================================

# Imports padrões
import logging

# Imports de terceiros
import pandas as pd

# Imports locais

# =================================================================================================================================================================
# Funções auxiliares
# =================================================================================================================================================================

def exportar_para_excel(data: list, filename: str) -> None:
    """
    Exporta dados para um arquivo Excel.

    Args:
        data (list): Lista de dicionários contendo os dados a serem exportados.
        filename (str): Nome do arquivo Excel de destino.
    """

    logging.info(f"Criando dataframe para exportar os dados.")
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    logging.info(f"Dados exportados para o arquivo {filename}.")


def return_updates(df1: pd.DataFrame, df2: pd.DataFrame, on: str, colunas: list, suffixes: tuple) -> pd.DataFrame:
    """
    Retorna as atualizações entre dois DataFrames. Recomendado para verificar as diferenças entre dois DataFrames que possuam um identificador único.

    Args:
        df1 (pd.DataFrame): DataFrame 1.
        df2 (pd.DataFrame): DataFrame 2.
        on (str): Coluna de junção.
        colunas (list): Colunas a serem comparadas.
        suffixes (tuple): Sufixos a serem utilizados.

    Returns:
        pd.DataFrame: DataFrame contendo as atualizações.

    Examples:
        >>> df1 = pd.DataFrame({
        ...     'id': [1, 2, 3],
        ...     'value': ['A', 'B', 'C'],
        ... })
        >>> df2 = pd.DataFrame({
        ...     'id': [2, 3, 4],
        ...     'value': ['B', 'C_updated', 'D'],
        ... })
        >>> diff_df = return_updates(df1, df2, "id", ["value"], ("_banco", "_modulacao"))
        >>> print(diff_df)
        >>>    id value_banco value_modulacao
        >>> 1   3           C       C_updated
        >>> 2   4         NaN               D
    """

    # Realiza a junção dos DataFrames de acordo com os parâmetros
    merged = pd.merge(df1, df2, on=on, how='outer', indicator=True, suffixes=suffixes)
    
    # Preenche valores nulos com vazio para evitar problemas na comparação
    merged = merged.replace({pd.NA: '', None: '', 'None': '', 'nan': ''})

    # Filtra as linhas que possuem diferenças baseadas nas colunas especificadas
    diff = pd.concat([merged[(merged[col + suffixes[0]] != merged[col + suffixes[1]])] for col in colunas])

    # Remove duplicatas devido à concatenação de linhas a cada coluna diferente entre os DataFrames
    diff = diff.drop_duplicates()

    # Retorna o dataframe contendo as atualizações
    return diff


def return_diff(df1: pd.DataFrame, df2: pd.DataFrame, colunas: list, source: tuple) -> pd.DataFrame:
    """
    Retorna as linhas únicas entre dois DataFrames. Recomendado para verificar a diferença em uma relação de muitos para muitos.

    Args:
        df1 (pd.DataFrame): DataFrame 1.
        df2 (pd.DataFrame): DataFrame 2.
        colunas (list): Colunas a serem comparadas.
        source (tuple): Tupla contendo o nome das fontes dos DataFrames.

    Returns:
        pd.DataFrame: DataFrame contendo as diferenças.

    Examples:
        >>> modulacoes_banco = pd.DataFrame({
        ...     'id': [1, 1, 1],
        ...     'description': ['A', 'B', 'C']
        ... })
        >>> modulacoes_mdl = pd.DataFrame({
        ...     'id': [1, 1, 1],
        ...     'description': ['A', 'B', 'D']
        ... })
        >>> modulacoes_banco['source'] = 'modulacoes_banco'
        >>> modulacoes_mdl['source'] = 'modulacoes_mdl'
        >>> diff_df = return_diff(modulacoes_banco, modulacoes_mdl, ('modulacoes_banco', 'modulacoes_mdl'))
        >>> print(diff_df)
        >>>    id description source
        >>> 2   1          C   modulacoes_banco
        >>> 2   1          D   modulacoes_mdl
    """

    # Adiciona uma coluna para identificar a origem dos dados
    df1['source'] = source[0]
    df2['source'] = source[1]

    # Substitui dados nulos por vazio para evitar problemas na comparação
    df1 = df1.replace({pd.NA: '', None: '', 'None': '', 'nan': ''})
    df2 = df2.replace({pd.NA: '', None: '', 'None': '', 'nan': ''})

    # Realiza a junção dos DataFrames
    diff = pd.concat([df1, df2]).drop_duplicates(subset=colunas, keep=False)

    # Retorna o dataframe contendo as diferenças
    return diff


def diff_to_return_updates(diff: pd.DataFrame, identificadores: list, sources: tuple, suffixes: tuple) -> pd.DataFrame:
    """
    Retorna as atualizações entre dois DataFrames a partir de um DataFrame de diferenças.

    Args:
        diff (pd.DataFrame): DataFrame de diferenças resultante da função return_diff.
        identificadores (list): Colunas de identificação para a junção dos DataFrames.
        sources (tuple): Tupla contendo o nome das fontes dos DataFrames.
        suffixes (tuple): Sufixos a serem utilizados para as diferentes fontes.

    Returns:
        pd.DataFrame: DataFrame contendo as atualizações.

    Examples:
        >>> diff = pd.DataFrame({
        ...     'id': [1, 1, 2],
        ...     'value': ['A', 'B', 'C'],
        ...     'source': ['banco', 'mdl', 'mdl']
        ... })
        >>> updates = diff_to_return_updates(diff, ["id"], ("banco", "mdl"), ("_banco", "_mdl"))
        >>> print(updates)
        >>>    id value_banco value_mdl
        >>> 1   1          A         B
        >>> 2   2          None      C
    """
    
    # Separa os registros
    df1 = diff[diff.source == sources[0]]
    df2 = diff[diff.source == sources[1]]

    # Junta os DataFrames
    df = pd.merge(df1, df2, on=identificadores, how="outer", suffixes=(suffixes[0], suffixes[1]), indicator=True)

    # Retorna o DataFrame contendo as atualizações
    return df


def update_to_html(df: pd.DataFrame, identificador: str, suffixes: tuple, colunas: list, indicator: str) -> None:
    """
    Exporta um DataFrame para um arquivo HTML.

    Args:
        df (pd.DataFrame): DataFrame a ser exportado.
        suffixes (tuple): Sufixos utilizados na comparação das colunas equivalentes.
        identificador (str): Coluna de identificação.
        colunas (list): Colunas a serem comparadas sem os sufixos.
        indicator (str): Coluna de indicador de diferenças do método pd.merge.

    Returns:
        str: Código HTML contendo a tabela customizada.

    Examples:
        >>> df = pd.DataFrame({
        ...     'id': [1, 2, 3],
        ...     'value_banco': [None, 'B', 'C'],
        ...     'value_modulacao': ['A_updated', 'B_updated', None],
        ...     '_merge': ['left_only', 'both', 'right_only']
        ... })
        >>> html = update_to_html(df, "id", ("_banco", "_modulacao"), ["value"], "_merge")
        >>> print(html)
        >>> <table class="table table-bordered">
        >>>     <thead>
        >>>         <tr>
        >>>             <th scope='col' class='table-secondary'>id</th>
        >>>             <th scope='col' class='table-secondary'>value</th>
        >>>         </tr>
        >>>     </thead>
        >>>     <tr class='table-danger'><td>1</td><td>None -> A_updated</td></tr>
        >>>     <tr class='table-primary'><td>2</td><td>B -> B_updated</td></tr>
        >>>     <tr class='table-success'><td>3</td><td>C</td></tr>
        >>> </table>
    """

    # Cria tabela html customizada com bootstrap 5.3 para destacar linhas com diferenças
    html = f"""
    <table class="table table-bordered">
        <thead>
            <tr>
    """

    # Adiciona os cabeçalhos das colunas
    for col in colunas:
        html += f"<th scope='col' class='table-secondary'>{col}</th>"

    # Fecha a linha do cabeçalho    
    html += "</tr>"

    # Se merge for right_only, adiciona a classe table-danger, se for both, adiciona a classe table-primary e se for left_only, adiciona a classe table-success na linha.
    for index, row in df.iterrows():
        html += "<tr class='"
        html += "table-danger" if row[indicator] == "left_only" else "table-primary" if row[indicator] == "both" else "table-success"
        html += " text-nowrap'>"
        for col in colunas:
            if col == identificador:
                html += f"<td>{row[col]}</td>"
            elif row[col + suffixes[0]] == row[col + suffixes[1]]:
                html += f"<td>{row[col + suffixes[0]]}</td>"
            else:
                html += f"<td>{row[col + suffixes[0]]} -> {row[col + suffixes[1]]}</td>"
        html += "</tr>"
        
    # Adiciona uma linha para indicar que não há diferenças se o DataFrame estiver vazio
    if df.empty:
        html += f"<tr><td colspan='{len(colunas)}'>Nenhuma alteração encontrada.</td></tr>"

    # Fecha a tabela
    html += """
        </thead>
    </table>
    """

    return html


def diff_to_html(df: pd.DataFrame, colunas: list, source: tuple) -> None:
    """
    Exporta um DataFrame para um arquivo HTML.

    Args:
        df (pd.DataFrame): DataFrame a ser exportado.
        colunas (list): Colunas a serem comparadas.
        source (tuple): Tupla contendo o nome das fontes dos DataFrames.

    Returns:
        str: Código HTML contendo a tabela customizada.

    Examples:
        >>> df = pd.DataFrame({
        ...     'id': [1, 2, 3],
        ...     'description': ['A', 'B', 'C'],
        ...     'source': ['banco', 'mdl', 'mdl']
        ... })
        >>> html = diff_to_html(df, ["id", "description"], ("banco", "analitico"))
        >>> print(html)
        >>> <table class="table table-bordered">
        >>>     <thead>
        >>>         <tr>
        >>>             <th scope='col' class='table-secondary'>id</th>
        >>>             <th scope='col' class='table-secondary'>description</th>
        >>>         </tr>
        >>>     </thead>
        >>>     <tr class='table-danger'><td>1</td><td>A</td></tr>
        >>>     <tr class='table-primary'><td>2</td><td>B</td></tr>
        >>>     <tr class='table-primary'><td>3</td><td>C</td></tr>
        >>> </table>
    """

    # Cria tabela html customizada com bootstrap 5.3 para destacar linhas com diferenças
    html = f"""
    <table class="table table-bordered">
        <thead>
            <tr>
    """

    # Adiciona os cabeçalhos das colunas
    for col in colunas:
        html += f"<th scope='col' class='table-secondary'>{col}</th>"

    # Fecha a linha do cabeçalho    
    html += "</tr>"

    # Se merge for right_only, adiciona a classe table-danger, se for both, adiciona a classe table-primary e se for left_only, adiciona a classe table-success na linha.
    for index, row in df.iterrows():
        html += "<tr class='"
        html += "table-danger" if row["source"] == source[0] else "table-success"
        html += " text-nowrap'>"
        for col in colunas:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"

    # Adiciona uma linha para indicar que não há diferenças se o DataFrame estiver vazio
    if df.empty:
        html += f"<tr><td colspan='{len(colunas)}'>Nenhuma alteração encontrada.</td></tr>"

    # Fecha a tabela
    html += """
        </thead>
    </table>
    """

    return html


def diff_updates_to_html(df: pd.DataFrame, identificadores: list = ["id"], colunas: list = ["id"], suffixes: tuple = ("_1", "_2"), indicator: str = "_merge") -> None:
    """
    Exporta um DataFrame para um arquivo HTML. 

    Args:
        df (pd.DataFrame): DataFrame a ser exportado.
        suffixes (tuple): Sufixos utilizados na comparação das colunas equivalentes.
        identificadores (list): Colunas de identificação para a junção dos DataFrames.
        colunas (list): Colunas a serem comparadas sem os sufixos.
        indicator (str): Coluna de indicador de diferenças do método pd.merge.

    Returns:
        str: Código HTML contendo a tabela customizada.

    Examples:
        >>> df = pd.DataFrame({
        ...     'id': [1, 2, 3],
        ...     'value_banco': [None, 'B', 'C'],
        ...     'value_modulacao': ['A_updated', 'B_updated', None],
        ...     '_merge': ['left_only', 'both', 'right_only']
        ... })
        >>> html = update_to_html(df, "id", ("_banco", "_modulacao"), ["value"], "_merge")
        >>> print(html)
        >>> <table class="table table-bordered">
        >>>     <thead>
        >>>         <tr>
        >>>             <th scope='col' class='table-secondary'>id</th>
        >>>             <th scope='col' class='table-secondary'>value</th>
        >>>         </tr>
        >>>     </thead>
        >>>     <tr class='table-danger'><td>1</td><td>None -> A_updated</td></tr>
        >>>     <tr class='table-primary'><td>2</td><td>B -> B_updated</td></tr>
        >>>     <tr class='table-success'><td>3</td><td>C</td></tr>
        >>> </table>
    """

    # Cria tabela html customizada com bootstrap 5.3 para destacar linhas com diferenças
    html = f"""
    <table class="table table-bordered">
        <thead>
            <tr>
    """

    # Adiciona os cabeçalhos das colunas
    for col in colunas:
        html += f"<th scope='col' class='table-secondary'>{col}</th>"

    # Fecha a linha do cabeçalho    
    html += "</tr>"

    # Se merge for right_only, adiciona a classe table-danger, se for both, adiciona a classe table-primary e se for left_only, adiciona a classe table-success na linha.
    for index, row in df.iterrows():
        html += "<tr class='"
        html += "table-danger" if row[indicator] == "left_only" else "table-primary" if row[indicator] == "both" else "table-success"
        html += " text-nowrap'>"
        for col in colunas:
            if col in identificadores:
                html += f"<td>{row[col]}</td>"
            elif row[indicator] == "right_only":
                html += f"<td>{row[col + suffixes[1]]}</td>"
            elif row[indicator] == "left_only":
                html += f"<td>{row[col + suffixes[0]]}</td>"
            elif row[indicator] == "both":
                if row[col + suffixes[0]] == row[col + suffixes[1]]:
                    html += f"<td>{row[col + suffixes[0]]}</td>"
                else:
                    html += f"<td>{row[col + suffixes[0]]} -> {row[col + suffixes[1]]}</td>"
        html += "</tr>"
        
    # Adiciona uma linha para indicar que não há diferenças se o DataFrame estiver vazio
    if df.empty:
        html += f"<tr><td colspan='{len(colunas)}'>Nenhuma alteração encontrada.</td></tr>"

    # Fecha a tabela
    html += """
        </thead>
    </table>
    """

    return html