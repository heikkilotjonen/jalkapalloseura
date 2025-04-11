from db import get_db_connection

def get_notices(page, page_size):
    connection = get_db_connection()
    sql = """SELECT n.id, n.title, COUNT(s.id) total 
            FROM notices n
            LEFT JOIN signings s ON n.id = s.notice_id
            GROUP BY n.id
            ORDER BY n.id DESC
            LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    notices = connection.execute(sql, [limit, offset]).fetchall()
    connection.close()
    return notices

def notice_count():
    connection = get_db_connection()
    sql = "SELECT COUNT(n.id) FROM notices n"
    search = connection.execute(sql)
    result = search.fetchone()[0]
    connection.close()
    return result

def get_notice(notice_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT n.id, n.title, n.content, n.user_id, u.username 
            FROM notices n, users u 
            WHERE n.user_id = u.id AND n.id = ?"""
    cursor.execute(sql, [notice_id])
    notice = cursor.fetchone()
    connection.close()
    return notice if notice else None

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
    sql2 = "DELETE FROM signings WHERE notice_id = ?"
    cursor.execute(sql, [notice_id])
    cursor.execute(sql2, [notice_id])
    connection.commit()
    connection.close()

def search(query):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """SELECT n.id notice_id,
                    n.title notice_title,
                    u.username
             FROM notices n, users u
             WHERE u.id = n.user_id AND
                   (n.content LIKE ? OR n.title LIKE ?)
             ORDER BY n.id DESC"""
    search = cursor.execute(sql, ["%" + query + "%", "%" + query + "%"])
    return search    

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
        return signing_id[0]  
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