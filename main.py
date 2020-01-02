from common import utils
from mainersql import MainerSQL
import json
LOGGER = utils.setting_log()

def main():
    database_conn = json.load(open('./database_connections.json'))
    query = "select getdate() as test"
    
    LOGGER.info('Connecting to database')
    msql = MainerSQL(database_conn.get('conn_test'))
    LOGGER.info('Executing query....')
    msql.execute_query(query)
    LOGGER.info('Persist query result')
    msql.persist_query()

if __name__ == "__main__":
    main()
