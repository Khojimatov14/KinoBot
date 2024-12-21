import sqlite3


class DatabaseMoviesInfo:
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

    def create_table_movies_info(self):
        sql = """
        CREATE TABLE MoviesInfo (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_name TEXT,
            movie_country TEXT,
            movie_year TEXT,
            movie_language TEXT,
            movie_time TEXT
            );
        """
        self.execute(sql, commit=True)

    def set_starting_movie_id(self, start_id=1000):
        sql = "UPDATE sqlite_sequence SET seq = ? WHERE name = 'MoviesInfo';"
        self.execute(sql, parameters=(start_id - 1,), commit=True)

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

    def add_movie(self, movie_name: str, movie_country: str, movie_year: str, movie_language: str, movie_time: str):
        sql = """
            INSERT INTO MoviesInfo (movie_name, movie_country, movie_year, movie_language, movie_time) VALUES (?, ?, ?, ?, ?)
            """
        self.execute(sql, parameters=(movie_name, movie_country, movie_year, movie_language, movie_time), commit=True)

    def update_movie_info(self, movie_id, **kwargs):
        sql = "UPDATE MoviesInfo SET "
        sql, parameters = self.formatArgs(sql, kwargs)
        sql += " WHERE movie_id = ?;"
        parameters += (movie_id,)
        return self.execute(sql, parameters=parameters, commit=True)

    def select_movie_info(self, **kwargs):
        sql = "SELECT * FROM MoviesInfo WHERE "
        sql, parameters = self.formatArgs(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_last_movie_info(self):
        sql = """
        SELECT * FROM MoviesInfo ORDER BY movie_id DESC LIMIT 1;
        """
        return self.execute(sql, fetchone=True)

    def get_all_movies_info(self):
        sql = """
        SELECT * FROM MoviesInfo ORDER BY movie_id DESC;
        """
        return self.execute(sql, fetchall=True)

    def delete_movie_by_id(self, movie_id: int):
        sql = "DELETE FROM MoviesInfo WHERE movie_id = ?;"
        self.execute(sql, parameters=(movie_id,), commit=True)


# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)