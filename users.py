from db import get_db_connection

def get_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "SELECT username FROM users WHERE id = ?"
    search = cursor.execute(sql, [user_id])
    result = search.fetchall()[0]
    return result if result else None

def get_own_notices(user_id, offset, page_size):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT n.id, n.title, n.date, n.location
             FROM notices n
             WHERE n.user_id = ?
             LIMIT ? OFFSET ?"""
    search = cursor.execute(sql, [user_id, page_size, offset])
    results = search.fetchall()
    return results

def own_notices_count(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT COUNT(n.id)
             FROM notices n
             WHERE n.user_id = ?"""
    search = cursor.execute(sql, [user_id])
    results = search.fetchall()[0][0]
    return results

def get_signed_notices(user_id, offset, page_size):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT n.id, n.title, n.date, n.location
             FROM notices n
             JOIN signings s ON n.id = s.notice_id
             WHERE s.user_id = ?
             LIMIT ? OFFSET ?"""
    search = cursor.execute(sql, [user_id, page_size, offset])
    results = search.fetchall()
    return results

def signed_notices_count(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT COUNT(n.id)
             FROM notices n
             JOIN signings s ON n.id = s.notice_id
             WHERE s.user_id = ?"""
    search = cursor.execute(sql, [user_id])
    results = search.fetchall()[0][0]
    return results