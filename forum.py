from db import get_db_connection

def get_notices():
    connection = get_db_connection()
    sql = """SELECT n.id, n.title, COUNT(s.id) total 
            FROM notices n
            LEFT JOIN signings s ON n.id = s.notice_id
            GROUP BY n.id
            ORDER BY n.id DESC"""
    notices = connection.execute(sql).fetchall()
    connection.close()
    return notices

def get_notice(notice_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT n.id, n.title, n.content, n.user_id, u.username 
            FROM notices n, users u 
            WHERE n.user_id = u.id AND n.id = ?"""
    cursor.execute(sql, [notice_id])
    notice = cursor.fetchone()
    connection.close()
    return notice


def add_notice(title, content, user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO notices (title, content, user_id) VALUES (?, ?, ?)"
    cursor.execute(sql, [title, content, user_id])
    notice_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return notice_id

def update_notice(notice_id, content):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "UPDATE notices SET content = ? WHERE id = ?"
    cursor.execute(sql, [content, notice_id])
    connection.commit()
    connection.close()

def remove_notice(notice_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM notices WHERE id = ?"
    cursor.execute(sql, [notice_id])
    connection.commit()
    connection.close()


def add_signing(user_id, notice_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO signings (user_id, notice_id) VALUES (?, ?)"
    cursor.execute(sql, [user_id, notice_id])
    signing_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return signing_id

def del_signing(signing_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM signings WHERE id = ?"
    cursor.execute(sql, [signing_id])
    connection.commit()
    connection.close()

def get_signings(notice_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT u.username FROM users u
             JOIN signings s ON u.id = s.user_id
             WHERE s.notice_id = ?
             ORDER BY s.id"""
    cursor.execute(sql, [notice_id])
    signings = cursor.fetchall()
    connection.close()
    return signings

def get_signing(notice_id, user_id):
    connection = get_db_connection()
    cursor = connection.cursor() 
    sql = """SELECT id FROM signings
            WHERE user_id = ? AND notice_id = ?"""
    cursor.execute(sql, [user_id, notice_id])
    signing_id = cursor.fetchone()
    connection.close()
    if signing_id:
        return signing_id[0]  # Palautetaan ensimmäinen elementti, joka on id
    else:
        return None

def is_user_signed_up(user_id, notice_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = "SELECT COUNT(*) FROM signings WHERE user_id = ? AND notice_id = ?"
    cursor.execute(sql, [user_id, notice_id])
    count = cursor.fetchone()[0]
    connection.close()
    return count > 0