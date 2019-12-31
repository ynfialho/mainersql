from os import getenv, remove as remove_file
import pyodbc
import csv
import re
import datetime
import pytz


class MainerSQL:
    """
    Abstraction of data extraction from DBMS.
    The current version includes:
    - Extraction: sql_server
    - Persistence: Local
    - Formats: CSV
    """
    def __init__(self, database_config):
        self.db_config = database_config
        self.conn = self.__get_connection()
        self.cursor = self.conn.cursor()
        self.tbl_name = None
        self.row = None
    
    def __get_connection(self):
        engine_map = dict()
        engine_map['sql_server'] = pyodbc.connect
        sql_engine = engine_map.get(self.db_config['type'])
        conn = sql_engine(self.db_config['conn_string'])
        return conn

    def __parse_table_name(self, _query):
        q = re.search(r'from\s+([^ ,]+)(?:\s*,\s*([^ ,]+))*', _query.lower())
        tbl_name = q.group()
        return tbl_name.split('.')[-1] if tbl_name else 'none'
    
    def __zip_file(self, file_path, zip_mode='w'):
        from zipfile import ZipFile, ZIP_DEFLATED
        zip_path = file_path.replace('.csv', '.zip')
        zfw = ZipFile(zip_path, zip_mode, compression=ZIP_DEFLATED)
        zfw.write(file_path, file_path.split('/')[-1])
        zfw.close()
        remove_file(file_path)
    
    def execute_query(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        self.tbl_name = self.__parse_table_name(query)
        self.row = row
        return row
    
    def persist_query(self, path=None, mode_write='w', sep='|', quote=csv.QUOTE_NONNUMERIC, flag_zip=False):
        if path:
            path_local = path
        else:
            ts = (datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))).strftime('%Y%m%d%H%M%S')
            path_local = './{tbl}_{ts}.csv'.format(tbl=self.tbl_name, ts=ts)

        with open(path_local, mode_write, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=sep, quoting=quote)
            writer.writerow([x[0] for x in self.cursor.description])
            while self.row:
                writer.writerow(self.row)
                self.row = self.cursor.fetchone()
        if flag_zip:
            self.__zip_file(path_local)


    