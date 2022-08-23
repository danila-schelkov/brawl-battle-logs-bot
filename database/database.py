import sqlite3


class Database:
    def __init__(self, filename: str):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def exists(self, table: str, column: str, value: str or int) -> bool:
        if type(value) is str:
            value = f'"{value}"'
        self.execute(f'SELECT EXISTS (SELECT 1 FROM {table} WHERE {column}={value} LIMIT 1)')
        exists = self.fetch()[0]
        return exists == 1

    def select(self, table: str,
               columns: list or str = None,
               condition: tuple = None,
               limit: int = -1) -> tuple or list:
        if columns is None:
            columns = []
        elif type(columns) is str:
            columns = [columns]

        query = f'SELECT {", ".join(columns) or "*"} from {table}'
        if condition is not None:
            column = condition[0]
            value = condition[1]
            if type(value) is str:
                value = f'"{value}"'

            query += f' WHERE {column}={value}'
        if limit > 0:
            query += f' LIMIT {limit}'
        self.execute(query)

        fetched = self.fetch()

        if len(columns) == 1 and type(fetched) is list:
            fetched = [row[0] for row in fetched]
        elif type(fetched) is tuple and len(fetched) == 1:
            fetched = fetched[0]
        elif len(fetched) != 0 and type(fetched) is not list:
            fetched = [fetched]

        return fetched

    def update(self, table: str,
               columns: list,
               condition: tuple or str,
               limit: int = -1):

        query = f'UPDATE {table} SET '
        for column_index in range(len(columns)):
            column, value = columns[column_index]
            if type(value) is str:
                value = f'"{value}"'
            elif value is None:
                value = 'null'

            if column_index > 0:
                query += ', '
            query += f'{column}={value}'
        if type(condition) is tuple:
            column, value = condition
            if type(value) is str:
                value = f'"{value}"'

            query += f' WHERE {column}={value}'
        else:
            query += f' WHERE {condition}'
        if limit > 0:
            query += f' LIMIT {limit}'
        self.execute(query)

    def execute(self, query: str):
        self.cursor.execute(f'{query};')

    def commit(self):
        self.connection.commit()

    def fetch(self):
        fetched = self.cursor.fetchall()

        if len(fetched) > 1:
            return fetched
        elif len(fetched) == 1:
            return fetched[0]

        return fetched

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        self.connection.close()
