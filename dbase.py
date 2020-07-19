import sqlite3
import os

db_name = '../db/botdbase.db'


def safety_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect(db_name, check_same_thread=False) as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    '''
    def inner(*args, **kwargs):
        with psycopg2.connect(dbname='botdbase', user='postgres',
                            password='12postgre05', host='192.168.1.5') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res
    '''

    return inner


@safety_connection
def init_db(conn):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    # conn = psycopg2.connect(dbname='botdbase', user='postgres',
                            # password='12postgre05', host='192.168.1.5')

    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users('
                   'token text NOT NULL, '
                   'user_id text NOT NULL, '
                   'chat_id text NOT NULL, '
                   'state integer NOT NULL, '
                   'PRIMARY KEY (token, user_id))')

    conn.commit()
    cursor.execute('CREATE TABLE IF NOT EXISTS bots(token text NOT NULL, '
                   'name text NOT NULL, '
                   'active integer NOT NULL, '
                   'pid text NOT NULL, '
                   'greetings text NOT NULL, '
                   'approval text NOT NULL, '
                   'unsubscribe text NOT NULL, '
                   'advice text NOT NULL, '
                   'change_name text NOT NULL, '
                   'PRIMARY KEY (token, name))')
    conn.commit()


@safety_connection
def get_chat_id_by_user_id(conn, token, user_id: str):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
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
def start_bot_dbase(conn, params):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("select token from bots where token='{token}'".format(token=params[1]))
    if len(cursor.fetchall()) != 0: # значит бот уже есть в таблице, его нужно запустить
        return 0
    conn.commit()
    cursor.execute("insert into bots (token, name, active, pid, greetings, approval, unsubscribe, advice, change_name) "
                   "values ('{token}', '{name}', {active}, '{pid}', '{greetings}', '{approval}', '{unsubscribe}', "
                   "'{advice}', '{change_name}')".format(token=params[0], name=params[1], active=str(0), pid='',
                                                         greetings=params[2], approval=params[3], unsubscribe=params[4],
                                                         advice=params[5], change_name=params[6]))
    conn.commit()
    cursor.close()
    return 0


@safety_connection
def get_pid(conn, name):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("select pid from bots where name='{name}'".format(name=name))
    (res,) = cursor.fetchall()
    conn.commit()
    return res[0]


@safety_connection
def get_all_pid(conn):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("select pid from bots")
    rows = cursor.fetchall()
    # print(rows)
    info = ''
    for row in rows:
        info += str(row[0]) + ','
    conn.commit()
    cursor.close()
    # print(info)
    return info[0:len(info) - 1]        # ВАЖНО ПРОТЕСТИТЬ


@safety_connection
def update_pid(conn, pid, name):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("update bots set pid = '{pid}' where name = '{name}'".format(pid=pid, name=name))
    conn.commit()
    cursor.close()


@safety_connection
def is_active(conn, name):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("select active from bots where name='{name}'".format(name=name))
    if len(cursor.fetchall()) == 0:
        return None
    conn.commit()
    cursor.execute("select active from bots where name='{name}'".format(name=name))
    (res,) = cursor.fetchall()
    # print('active = ' + str(res[0]))
    conn.commit()
    cursor.close()
    return int(res[0])


@safety_connection
def update_active(conn, name, active):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("update bots set active = {active} where name = '{name}'".format(active=active, name=name))
    conn.commit()
    cursor.close()


@safety_connection
def get_token(conn, name):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    # print(name)
    cursor.execute("select token from bots where name='{name}'".format(name=name))
    if len(cursor.fetchall()) == 0:
        return None
    conn.commit()
    # print(name)
    cursor.execute("select token from bots where name='{name}'".format(name=name))
    (res,) = cursor.fetchall()
    conn.commit()
    cursor.close()
    # print(res)
    return res[0]


@safety_connection
def get_column(conn, name, column):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("select {column} from bots where name='{name}'".format(column=column, name=name))
    if len(cursor.fetchall()) == 0:
        return None
    conn.commit()
    cursor.execute("select {column} from bots where name='{name}'".format(column=column, name=name))
    (res,) = cursor.fetchall()
    conn.commit()
    cursor.close()
    return res[0]


@safety_connection
def update_column(conn, name, column, content):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("update bots set {column} = '{content}' where name='{name}'".format(column=column,
                                                                                       content=content, name=name))
    conn.commit()
    cursor.close()


@safety_connection
def get_all_table(conn):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("select * from bots")
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    info = ''
    for row in rows:
        info += str(row[0]) + ' ' + row[1] + ' ' + str(row[2]) + ' ' + str(row[3]) + ' ' + str(row[4]) \
                + ' ' + str(row[5]) + ' ' + str(row[6]) + ' ' + str(row[7]) + ' ' + str(row[8]) + '\n'
    return info


@safety_connection
def drop(conn):
    # conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("drop table bots")
    conn.commit()
    cursor.execute("drop table users")
    conn.commit()
    cursor.close()


@safety_connection
def get_all_chat_id(conn, token):
    cursor = conn.cursor()
    cursor.execute("select chat_id from users where token='{token}'".format(token=token))
    if len(cursor.fetchall()) == 0:
        return None
    cursor.execute("select chat_id from users where token='{token}'".format(token=token))
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    res = []
    for row in rows:
        res.append(row[0])
    return res


def progress(status, remaining, total):
    print(f'Copied {total-remaining} of {total} pages...')


def make_backup(path_to_db, path_to_backup):
    try:
        # existing DB
        sqlite_con = sqlite3.connect(path_to_db)
        # copy into this DB
        if not os.path.exists(path_to_backup):
            open(path_to_backup, 'w').close()
        backup_con = sqlite3.connect(path_to_backup)
        with backup_con:
            sqlite_con.backup(backup_con, pages=1, progress=progress)
        print("backup successful")
        backup_con.close()
        sqlite_con.close()
    except sqlite3.Error as error:
        print("Error while taking backup: ", error)
