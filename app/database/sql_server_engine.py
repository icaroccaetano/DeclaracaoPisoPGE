from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_sql_server_engine():
    """
    Function to get a engine

    Returns a engine from the DB in .env BIGDATA_DB_CONNECTION_STRING
    """
    engine = create_engine(os.getenv('STRING_SQL_SERVER'))
    
    return engine