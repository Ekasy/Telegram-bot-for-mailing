import os
import json
import sys
import platform


def split_string(s):
    if platform.system() == 'Windows':
        return s.split('\\')
    else:
        return s.split('/')


def join_list(l):
    if platform.system() == 'Windows':
        return '\\'.join(l)
    else:
        return '/'.join(l)


def create_db(name_db='', proxy_s=''):
    path = split_string(os.getcwd())
    path.append('settings.json')

    with open(join_list(path), 'r') as f:
        data = json.load(f)
    if name_db == '':
        name_db = data['database']['name'] if data['database']['name'] != '' else 'botdbase.db'
    if proxy_s == '':
        proxy_s = data['proxy'] if data['proxy'] != '' else 'socks5h://geek:socks@t.geekclass.ru:7777'
    name_backup = '{name_db}_backup.db'.format(name_db=name_db[0:len(name_db)-3])

    path = path[0:len(path) - 1]
    path.append(name_db)
    path1 = join_list(path)
    if not os.path.exists(path1):
        open(path1, 'w').close()
    path = path[0:len(path) - 1]
    path.append(name_backup)
    path2 = join_list(path)
    if not os.path.exists(path2):
        open(path2, 'w').close()

    path = path[0:len(path) - 1]
    path.append('settings.json')

    with open(join_list(path), 'r') as f:
        data = json.load(f)
    data['database']['name'] = name_db
    data['database']['path'] = path1
    data['proxy'] = proxy_s
    with open(join_list(path), 'w') as f:
        json.dump(data, ensure_ascii=False, indent=4, fp=f)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        create_db()
    elif len(sys.argv) == 3:
        create_db(name_db=sys.argv[1], proxy_s=sys.argv[2])
    else:
        print('Слишком много параметров')
