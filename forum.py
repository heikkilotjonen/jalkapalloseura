from db import get_db_connection

def get_notices():
    connection = get_db_connection()
    sql = """SELECT n.id, n.title
             FROM notices n
             GROUP BY n.id
             ORDER BY n.id DESC"""
    notices = connection.execute(sql).fetchall()
    connection.close()
    return notices

def get_notice(notice_id):
    connection = get_db_connection()
    sql = "SELECT id, title FROM notices WHERE id = ?"
    return connection.execute(sql, [notice_id])


def add_notice(title, content, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO notices (title, content, user_id) VALUES (?, ?, ?)"
    cursor.execute(sql, [title, content, user_id])
    notice_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return notice_id