import db

def create_user(username, age):
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, age) VALUES (?, ?)', (username, age))
        conn.commit()
        return 'User created successful!'
    except Exception as e:
        return f'Unknown error: {e}'
    finally:
        conn.close()

def read_user(username):
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        user = cursor.fetchone()
        if user:
            return f'User {user} exists'
        else:
            return f'User {user} not found'
    except Exception as e:
        return f'Error: {e}'
    finally:
        conn.close()

def read_users():
    try:
        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        if users:
            msg = '\n'.join(str(user).strip() for user in users)
            msg = str(msg)
            return msg
        else:
            return 'No users'
    except Exception as e:
        return f'Error: {e}'
    finally:
        conn.close()

def update_user(username, age):
    try:
        conn=db.get_db_connection()
        cursor=conn.cursor()
        cursor.execute('UPDATE users SET age=? WHERE username=?', (age, username))
        conn.commit()
        return f'User {username} updated successful'
    except Exception as e:
        return f'Error: {e}'
    finally:
        conn.close()

def delete_user(username):
    try:
        conn=db.get_db_connection()
        cursor=conn.cursor()
        cursor.execute('DELETE FROM users WHERE username=?', (username,))
        conn.commit()
        return f'User {username} deleted successful'
    except Exception as e:
        return f'Error: {e}'
