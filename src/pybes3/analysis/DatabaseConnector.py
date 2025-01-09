import pymysql


class DatabaseConnector:
    def __init__(self, host: str, user: str, passwd: str):
        self._conn = pymysql.connect(host=host, user=user, passwd=passwd)

        assert self._conn.open, "Connection failed"

    def query(self, query: str) -> list[tuple]:
        cursor = self._conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
