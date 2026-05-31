import pymysql

def get_connection():
    try:
        return pymysql.connect(
            host='localhost',
            user='flaskuser',
            password='123flask',
            database='db_sxf',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as err:
        print(f"Erro MySQL: {err}")
        return None


def query_db(query, args=(), one=False):
    try:
        con = get_connection()
        if con is None:
            return None
        cursor = con.cursor()
        cursor.execute(query, args)
        result = cursor.fetchone() if one else cursor.fetchall()
        cursor.close()
        con.close()
        return result
    except Exception as e:
        print(f"ERRO MYSQL: {e}")
        return None
