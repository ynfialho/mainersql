# MainerSQL

Data extraction framework from DBMS

### Installing
The project is developed in a Ubuntu 19.04 environment and it is necessary that the unixodbc installed.

```shell
sudo apt install unixodbc-dev && \
git clone https://github.com/ynfialho/mainersql && \
cd mainersql && \
python3 -m pip install -r requirements.txt
```

### Usage
#### Configuration
With a simple JSON configuration, MainerSQL is ready for use.

```json
{
    "conn_dev":{
        "type":"mssql",
        "conn_string": "DRIVER={ODBC Driver 17 for SQL Server};SERVER=test;DATABASE=dbtest;UID=user;PWD=password"
    }
}
```
#### Run
```python
from mainersql import MainerSQL
import json
database_conn = json.load(open('./database_connections.json'))
query = "select getdate() as test"

msql = mainersql.MainerSQL(database_conn.get('conn_test'))
msql.execute_query(query)
msql.persist_query()
```

### Coverage
MainerSQL covers the following DBMS, locations, and formats;

<table>
	<thead>
		<tr>
			<th colspan="2">DBMS</th>
		</tr>
	</thead>
	<tbody>
		<tr><td style="text-align: center; height=40px;"><img height="40" src="https://cdn.worldvectorlogo.com/logos/microsoft-sql-server.svg" />                                    </td><td style="width: 0px;">SQL Server</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2">Locations</th>
		</tr>
	</thead>
	<tbody>
		<tr><td style="text-align: center; height=40px;"><img height="40" src="https://image.flaticon.com/icons/svg/567/567800.svg" />                                    </td><td style="width: 0px;">File System</tr>
	</tbody>
</table>

<table>
	<thead>
		<tr>
			<th colspan="2">Formats</th>
		</tr>
	</thead>
	<tbody>
		<tr><td style="text-align: center; height=40px;"><img height="40" src="https://image.flaticon.com/icons/png/512/1263/1263920.png" />                                    </td><td style="width: 0px;">CSV</tr>
	</tbody>
</table>