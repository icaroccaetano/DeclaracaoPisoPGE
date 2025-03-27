import pyodbc
import os
import pandas as pd

def criar_planilha_nao_encontrados():
    conn = pyodbc.connect(os.getenv('STRING_ACCES'))
    sql = ("""
        SELECT 
            DISTINCT cpf, 
            nome,
            ok as status
        FROM 
            BuscarVinculos 
        WHERE 
            rodou = FALSE
        """)
    df_relatorio = pd.read_sql(sql, conn)
    #Criando a planilha
    try:
        caminho_arquivo = os.path.expanduser(r'~/Desktop/NaoEncontrados24-02.xlsx')
        df_relatorio.to_excel(caminho_arquivo, index=False)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()