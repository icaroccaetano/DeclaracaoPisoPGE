from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def get_access_engine(query: str) -> pd.DataFrame:
    """
    Function to get the data from the Access database

    Returns a DataFrame with the data from the Access database
    """
    db_path = os.getenv('STRING_ACCES')
    connection_string = r"access+pyodbc:///?odbc_connect=Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + db_path

    engine = create_engine(os.getenv('STRING_ACCES'))
    
    return engine