import logging

from dao.db_session import global_db_init
from db import DATABASE_NAME
from services.process_service import process_query
from strings import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    global_db_init(f"db/{DATABASE_NAME}")
    print(INSTRUCTIONS)
    process_query()
