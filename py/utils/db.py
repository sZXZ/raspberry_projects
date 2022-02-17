from clickhouse_driver import Client
import pandas as pd
from pathlib import Path


class DB(Client):
    DB_HOST = "localhost"
    DB_PORT = 9000
    DB_USER = "default"
    DB_NAME = "default"
    CACHE_DEFAULT_PATH = Path(__file__).parent

    def __init__(
        self,
        host: str = DB_HOST,
        port: int = DB_PORT,
        user: str = DB_USER,
        database: str = DB_NAME,
        cache_path: Path = CACHE_DEFAULT_PATH,
        *args,
        **kwargs,
    ):
        super().__init__(
            host=host, port=port, user=user, database=database, *args, **kwargs
        )
        self.cache_path = cache_path
        self.cache_folder = self.cache_path.joinpath("cache")
        self.cache_folder.mkdir(exist_ok=True)
        self.formats_dict = {"int64": "Int64", "object": "String"}
        self.formats_convert = {"object": "String"}

    def create_db(self, database):
        return self.execute(f"CREATE DATABASE IF NOT EXISTS {database}")

    def drop_table(self, table):
        self.execute(f"DROP TABLE IF EXISTS {table}")

    def create_table_form_df(
        self, table_name: str, df: pd.DataFrame, order_column: str
    ):
        groups = df.columns.to_series().groupby(df.dtypes).groups
        schema = []
        insert_schema = []
        for key in groups.keys():
            for column in groups[key]:
                schema.append(f"{column} {self.formats_dict[str(key)]}")
                insert_schema.append(f"{column}")
        query = f"""
create table if not exists {table_name} ({','.join(schema)})
engine = MergeTree ORDER BY {order_column}
SETTINGS index_granularity = 8192
"""
        print(query)
        self.execute(query)
        query = f"""
insert into {table_name} {','.join(insert_schema)} values 
"""
        self.insert_df(table_name, df)

    def insert_df(self, table_name: str, df: pd.DataFrame):
        #groups = df.columns.to_series().groupby(df.dtypes).groups
        #insert_schema = df.columns.to_series().to_list()
        #formats = []
        
        groups = df.columns.to_series().groupby(df.dtypes).groups
        schema = []
        insert_schema = []
                
        inserts = []
        first = True
        for index, row in df.iterrows():
            line = []
            for key in groups.keys():
                for column in groups[key]:
                    if key == 'object':
                        line.append(f"'{row[column]}'")
                    else:
                        line.append(f"{row[column]}")
                    
                    schema.append(f"{column} {self.formats_dict[str(key)]}")
                    if first:
                        insert_schema.append(f"{column}")
            inserts.append(f"({','.join(line)})")
            first = False
        query = f"""
insert into {table_name} ({','.join(insert_schema)}) values {','.join(inserts)}
"""
        print(query)
        self.execute(query)
