from common import utils, mainer_sql
from common import constants as cs
import json
LOGGER = utils.setting_log()

def main():
    database_conn = json.load(open('./database_connections.json'))
    query = "select getdate() as test"
    
    LOGGER.info('Connecting to database')
    mainersql = mainer_sql.MainerSQL(database_conn.get('conn_test'))
    LOGGER.info('Executing query....')
    mainersql.execute_query(query)
    LOGGER.info('Persist query result')
    mainersql.persist_query()

if __name__ == "__main__":
    main()
