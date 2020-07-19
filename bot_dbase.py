import sqlite3
import config


db_name = config.PATH_TO_DB
# print('ds ' + db_name)


def safety_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect(db_name, check_same_thread=False) as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@safety_connection
def init_db(conn):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users('
                   'token text NOT NULL, '
                   'user_id text NOT NULL, '
                   'chat_id text NOT NULL, '
                   'state integer NOT NULL, '
                   'PRIMARY KEY (token, user_id))')
    conn.commit()
    cursor.close()


@safety_connection
def insert_id_into_table(conn, token, chat_id):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE token = '{token}' and chat_id = '{chat_id}'".
                   format(chat_id=chat_id, token=token))
    count = cursor.fetchone()[0]
    if not count:
        cursor.execute("insert into users (token, user_id, chat_id, state) values ('{token}', '{user_id}', "
                       "'{chat_id}', '{state}')".format(token=token, user_id=chat_id, chat_id=chat_id, state=0))
    conn.commit()
    cursor.close()


@safety_connection
def update_user_id(conn, token, chat_id: int, user_id: str):
    cursor = conn.cursor()
    cursor.execute("select user_id from users where token='{token}' and chat_id='{chat_id}'"
                   .format(token=token, chat_id=chat_id))
    (current_user_id,) = cursor.fetchall()
    conn.commit()
    cursor.execute("select user_id from users where token='{token}' and user_id='{user_id}'"
                   .format(token=token, user_id=user_id))
    res = cursor.fetchall()
    if len(res) != 0:
        return 'your' if current_user_id[0] == user_id else 'engaged'
    cursor.execute("update users set user_id='{user_id}' where token = '{token}' and chat_id='{chat_id}'"
                   .format(user_id=user_id, token=token, chat_id=chat_id))
    conn.commit()
    cursor.close()
    return 'replaced'


@safety_connection
def update_user_state(conn, token, chat_id: int, user_state: int):
    cursor = conn.cursor()
    cursor.execute("update users set state={state} where token='{token}' and chat_id='{chat_id}'".
                   format(state=user_state, token=token, chat_id=chat_id))
    conn.commit()
    cursor.close()


@safety_connection
def get_chat_id_by_user_id(conn, token, user_id: str):
    cursor = conn.cursor()
    cursor.execute("select chat_id from users where token='{token}' and user_id='{user_id}'".
                   format(token=token, user_id=user_id))
    if len(cursor.fetchall()) == 0:
        return None
    cursor.execute("select chat_id from users where token='{token}' and user_id='{user_id}'".
                   format(token=token, user_id=user_id))
    (res,) = cursor.fetchall()
    conn.commit()
    cursor.close()
    return res[0]


@safety_connection
def get_state_by_chat_id(conn, token, chat_id: int):
    cursor = conn.cursor()
    cursor.execute("select state from users where token='{token}' and chat_id='{chat_id}'".
                   format(token=token, chat_id=chat_id))
    (res,) = cursor.fetchall()
    conn.commit()
    cursor.close()
    return res[0]


@safety_connection
def user_is_exist(conn, token, chat_id):
    cursor = conn.cursor()
    cursor.execute("select chat_id from users where token='{token}' and chat_id='{chat_id}'".
                   format(token=token, chat_id=chat_id))
    return len(cursor.fetchall()) != 0


@safety_connection
def get_column(conn, token, column):
    cursor = conn.cursor()
    cursor.execute("select {column} from bots where token='{token}'".
                   format(column=column, token=token))
    (res,) = cursor.fetchall()
    conn.commit()
    cursor.close()
    return res[0]


@safety_connection
def unsubscribe(conn, token, chat_id):
    cursor = conn.cursor()
    cursor.execute("delete from users where token='{token}' and chat_id='{chat_id}'".
                   format(token=token, chat_id=chat_id))
    conn.commit()
    cursor.close()


@safety_connection
def get_info(conn):
    cursor = conn.cursor()
    cursor.execute("select * from users")
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    info = ''
    for row in rows:
        info += str(row[0]) + ' ' + row[1] + ' ' + str(row[2]) + ' ' + str(row[3]) + '\n'
    return info


@safety_connection
def drop(conn):
    cursor = conn.cursor()
    cursor.execute("drop table users")
    conn.commit()
    cursor.close()
