import sqlite3


class DatabaseMovies:
    def __init__(self, path_to_db="allData.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        with sqlite3.connect(self.path_to_db) as connection:
            # connection.set_trace_callback(logger)
            cursor = connection.cursor()
            data = None
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        return data

    def create_table_movies(self):
        sql = """
        CREATE TABLE Movies (
            movie_id INTEGER,
            movie_format TEXT,
            movie_file_id TEXT
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def formatArgs(sql, parameters: dict):
        if len(parameters) == 1:
            bat = " AND "
        else:
            bat = ", "
        sql += bat.join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_movie(self, movie_id: int, movie_format: str, movie_file_id: str):
        sql = """
            INSERT INTO Movies (movie_id, movie_format, movie_file_id) VALUES (?, ?, ?)
            """
        self.execute(sql, parameters=(movie_id, movie_format, movie_file_id), commit=True)

    def update_movie_info(self, movie_id, **kwargs):
        sql = "UPDATE Movies SET "
        sql, parameters = self.formatArgs(sql, kwargs)
        sql += " WHERE movie_id = ?;"
        parameters += (movie_id,)
        return self.execute(sql, parameters=parameters, commit=True)

    def select_movie_by_id(self, **kwargs):
        sql = "SELECT * FROM Movies WHERE "
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_movie_by_format(self, movie_id: int, movie_format: str):
        sql = "SELECT * FROM Movies WHERE movie_id = ? AND movie_format = ?"
        parameters = (movie_id, movie_format)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def delete_movies_by_id(self, movie_id: int):
        sql = "DELETE FROM Movies WHERE movie_id = ?;"
        self.execute(sql, parameters=(movie_id,), commit=True)


# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)