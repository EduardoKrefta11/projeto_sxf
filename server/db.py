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

    con = None
    cursor = None

    try:
        con = get_connection()

        if con is None:
            return None
        
        cursor = con.cursor()

        cursor.execute(query, args)

        result = cursor.fetchone() if one else cursor.fetchall()

        return result
    
    except Exception as e:

        print(f"ERRO MYSQL: {e}")

        return None
    
    finally:

        if cursor:
            cursor.close()
        if con:
            con.close()

def execute_db(query, args=(), one=False):

    con = None
    cursor = None

    try:
        con = get_connection()

        if con is None:
            return None
        
        cursor = con.cursor()

        cursor.execute(query, args)

        con.commit()

        return True
    
    except Exception as e:

        print(f"ERRO MYSQL: {e}")

        return None
    
    finally:

        if cursor:
            cursor.close()
        if con:    
            con.close()