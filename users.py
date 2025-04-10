from db import get_db_connection

def get_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "SELECT username FROM users WHERE id = ?"
    search = cursor.execute(sql, [user_id])
    result = search.fetchall()[0]
    return result if result else None

def get_signings(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT s.id,
                    s.notice_id,
                    s.user_id,
                    n.title notice_title
             FROM notices n, signings s
             WHERE n.id = s.notice_id AND n.user_id <> s.user_id AND
                   n.user_id = ?"""
    search = cursor.execute(sql, [user_id])
    results = search.fetchall()
    return results