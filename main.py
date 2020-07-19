import sys
import json
import subprocess
import time
import os
import platform
import signal
import dbase, bot_helper
import re


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


def sending(phones, message, bot_token):
    proxy_s = get_proxy()
    bot = bot_helper.Bot(bot_token, proxy_s)
    for phone in phones:
        user_id = dbase.get_chat_id_by_user_id(token=bot_token, user_id=phone)
        if user_id is not None:
            bot.send_message(user_id, message)


def sending_all(bot_token, chats_id, message):
    proxy_s = get_proxy()
    bot = bot_helper.Bot(bot_token, proxy_s)
    for chat_id in chats_id:
        bot.send_message(chat_id, message)
    return 'ok'


def process(name):
    path = split_string(os.path.abspath(sys.argv[0]))[0:-1]
    path.append('mybot.exe')
    bd_path = join_list(split_string(get_path_to_db()))
    proxy_s = get_proxy()
    if bd_path == 'error' or proxy_s == 'error':
        return 'error'
    # запускаю бота и жду 2 секунды, чтобы процесс точно запустился
    process_name = '/'.join(path)
    bot_token = dbase.get_token(name=name)
    time.sleep(0.5)
    if platform.system() == 'Linux':

        process_name = '/'.join(path).replace('.exe', '.py')
        proc = subprocess.Popen('python3 {program} "{token}" "{path_to_db}" "{proxy_s}" > outpu.txt &'.
                                format(program=process_name, token=bot_token, path_to_db=bd_path, proxy_s=proxy_s),
                                stdout=subprocess.PIPE, shell=True)

        '''
        process_name = process_name[0:-4]
        L=process_name.split('/')
        nname = './'+L[-1]
        L[-1] = nname
        process_name = '/'.join(L)
        proc = subprocess.Popen('{program} "{token}" "{path_to_db}" "{proxy_s}" > output.txt &'.
                                format(program=process_name, token=bot_token, path_to_db=bd_path,
                                       proxy_s=proxy_s), stdout=subprocess.PIPE, shell=True)
        '''
        time.sleep(2)
        proc = subprocess.Popen('ps',stdout=subprocess.PIPE, shell=True)
        res = proc.stdout.read().decode("utf-8", errors='ignore')
        l = res.split('\n')[1:]
        ls = []
        for i in l:
            ls.append(re.sub(r'\s+', ' ', i)[1:])
        ls = ls[0:-1]
        nname  = 'mybot'
        pid = []
        for i in ls:
            if i.split(' ')[3] == nname:
                pid.append(i.split(' ')[0])
        pids = dbase.get_all_pid().split(',')
        for p in pids:
            if p in pid:
                pid.pop(pid.index(p))
        dbase.update_pid(pid=','.join(pid), name=name)
        dbase.update_active(name=name, active=1)
        return 'ok'

    '''
    output = subprocess.Popen('python {program} "{token}" "{path_to_db}" "{proxy_s}" /b'.format(program=process_name, 
                                                                                                token=bot_token, 
                                                                                                path_to_db=bd_path, 
                                                                                                proxy_s=proxy_s), 
                              stdout=subprocess.PIPE, shell=True)
    '''
    output = subprocess.Popen('start /b {program} "{token}" "{path_to_db}" "{proxy_s}"'.format(program=process_name,
                                                                                               token=bot_token,
                                                                                               path_to_db=bd_path,
                                                                                               proxy_s=proxy_s),
                              stdout=subprocess.PIPE, shell=True)
    time.sleep(2)
    # обновляю process_name засовывая туда 'mybot.exe'
    process_name = process_name.split('/')[-1]

    # запрашиваю список запущенных процессов и ищу все с именем process_name
    output = subprocess.Popen('tasklist /fo csv /nh', stdout=subprocess.PIPE)
    res = output.stdout.read().decode("utf-8", errors='ignore')
    l = res.split('\r\n')
    pid = []
    for i in l:
        if '"' + process_name + '"' in i:
            spisok = i[1:len(i) - 2].split('","')
            pid.append(str(spisok[1]))
    pids = dbase.get_all_pid().split(',')
    for p in pids:
        if p in pid:
            pid.pop(pid.index(p))
    dbase.update_pid(pid=','.join(pid), name=name)
    dbase.update_active(name=name, active=1)
    return 'ok'


def start_bot(params):
    act = dbase.is_active(name=params[1])
    if act is not None:
        if act == 1:
            print('Бот уже включен')
            return 'ok'
        elif act == 0:
            dbase.update_column(name=params[1], column='greetings',
                                content=params[2] if params[2] != '' else 'Приветствую тебя! Если ты написал мне, то '
                                                                          'хочешь получать рассылку. Оставь свой '
                                                                          'контакт, чтобы я запомнил тебя')
            dbase.update_column(name=params[1], column='approval',
                                content=params[3] if params[3] != '' else 'Я запомнил тебя!')
            dbase.update_column(name=params[1], column='unsubscribe',
                                content=params[4] if params[4] != '' else 'Ты отписался от рассылки')
            dbase.update_column(name=params[1], column='advice',
                                content=params[5] if params[5] != '' else 'Введите команду /start, '
                                                                          'чтобы подписаться на рассылку')
            dbase.update_column(name=params[1], column='change_name',
                                content=params[6] if params[6] != '' else 'Введенное имя уже занято. Введите другое')
            return process(params[1])

    params[2] = params[2] if params[2] != '' else 'Приветствую тебя! Если ты написал мне, то хочешь получать ' \
                                                  'рассылку. Оставь свой контакт, чтобы я запомнил тебя'
    params[3] = params[3] if params[3] != '' else 'Я запомнил тебя!'
    params[4] = params[4] if params[4] != '' else 'Ты отписался от рассылки'
    params[5] = params[5] if params[5] != '' else 'Введите команду /start, чтобы подписаться на рассылку'
    params[6] = params[6] if params[6] != '' else 'Введенное имя уже занято. Введите другое'
    if dbase.start_bot_dbase(params=params) != 0:
        return 'error'
    return process(params[1])


def stop_bot(name):
    if platform.system() == 'Linux':
        pid = dbase.get_pid(name=name)
        if pid == '':
            print("Bot is not working")
            return 'ok'
        try:
            for p in pid.split(','):
                os.kill(int(p), signal.SIGKILL)
        except OSError:
            print('Bot is not working')
        dbase.update_pid(pid='', name=name)
        dbase.update_active(name=name, active=0)
        return 'ok'

    # запрашиваю список запущенных процессов и ищу все с именем process_name
    output = subprocess.Popen('tasklist /fo csv /nh', stdout=subprocess.PIPE)
    res = output.stdout.read().decode("utf-8", errors='ignore')
    l = res.split('\r\n')
    pid = []
    for i in l:
        if '"mybot.exe"' in i:
            spisok = i[1:len(i) - 2].split('","')
            pid.append(str(spisok[1]))
    pids = dbase.get_pid(name=name)
    for p in pids.split(','):
        if p in pid:
            subprocess.Popen('taskkill /pid ' + p + ' /f', stdout=subprocess.PIPE, shell=True)
    dbase.update_pid(pid='', name=name)
    dbase.update_active(name=name, active=0)
    return 'ok'


def get_path_to_db():
    path = split_string(os.path.abspath(sys.argv[0]))
    path = path[0:len(path) - 1]
    path.append('db')
    path.append('settings.json')

    with open(join_list(path), 'r') as f:
        data = json.load(f)
    return data['database']['path'] if data['database']['path'] != '' else 'error'


def get_proxy():
    path = split_string(os.path.abspath(sys.argv[0]))
    path = path[0:len(path) - 1]
    path.append('db')
    path.append('settings.json')

    with open(join_list(path), 'r') as f:
        data = json.load(f)
    return data['proxy'] if data['proxy'] != '' else 'error'


def open_json(path):
    try:
        with open(join_list(split_string(path)), 'r', encoding="utf-8") as f:
            data = json.loads(f.read().encode(encoding="utf-8"))
            new_data = {}
            new_data['greetings'] = data['greetings']
            new_data['approval'] = data['approval']
            new_data['unsubscribe'] = data['unsubscribe']
            new_data['advice'] = data['advice']
            new_data['change_name'] = data['change_name']
            return new_data
    except:
        return {}


if __name__ == "__main__":
    dbase.db_name = join_list(split_string(get_path_to_db()))
    dbase.init_db()

    if len(sys.argv) == 1:
        print('Вы ввели недостаточно параметров')

    # запуск бота
    if sys.argv[1] == 'start':
        path_to_db = join_list(split_string(get_path_to_db()))
        proxy_s = get_proxy()
        if path_to_db != 'error' and proxy_s != 'error':
            # argv содержит строку вида: main.exe start token file.json
            if len(sys.argv) == 4:
                bot = bot_helper.Bot(sys.argv[2], proxy_s)
                name = bot.get_bot_name()
                del bot

                if name == 'not exist':
                    print('Произошла ошибка, проверьте токен бота')
                elif not os.path.exists(sys.argv[-1]):
                    print('Указанного файла не существует')
                elif sys.argv[-1].split('.')[-1] != 'json':
                    print('Файл не имеет разрешения json')
                elif open_json(sys.argv[-1]) == {}:
                    print('Неверное содержимое файла')
                else:
                    data = open_json(sys.argv[-1])
                    if start_bot([sys.argv[2], name, data['greetings'], data['approval'], data['unsubscribe'],
                                  data['advice'], data['change_name']]) == 'ok':
                        print('Бот ' + name + ' запущен')
                    else:
                        print('Произошла ошибка')

            # argv содержит строку вида: main.exe start bot_name
            if len(sys.argv) == 3:
                act = dbase.is_active(name=sys.argv[2])
                if act is not None:
                    if act == 1:
                        print('Бот уже включен')
                    elif act == 0:
                        if process(sys.argv[2]) == 'ok':
                            print('Бот ' + sys.argv[2] + ' запущен')
                        else:
                            print('Произошла ошибка')
                else:
                    print('Бот не найден')

            #print(dbase.get_all_table())
        else:
            print('Не указан путь к используемой базе данных')

    # argv содержит строку вида: main.exe stop bot_name
    elif sys.argv[1] == 'stop':
        if len(sys.argv) == 3:
            if dbase.get_token(name=sys.argv[2]) is None:
                print('Бот не найден')
            elif stop_bot(sys.argv[2]) == 'ok':
                print('Бот ' + sys.argv[2] + ' остановлен')
            else:
                print('Произошла ошибка')
        #print(dbase.get_all_table())

    # argv содержит строку вида: main.exe backup [db_path - путь до database куда копировать]
    elif sys.argv[1] == 'backup':
        path_to_db = join_list(split_string(get_path_to_db()))
        k = split_string(path_to_db)[0:-1]
        k.append('{name}_backup.db'.format(name=split_string(path_to_db)[-1][0:len(split_string(path_to_db)[-1]) - 3]))
        path_to_backup = join_list(k)
        if len(sys.argv) == 3:
            path_to_backup = sys.argv[2]
        dbase.make_backup(path_to_db, path_to_backup)

    # argv содержит строку вида: main.exe rollback [db_path - путь до database откуда копировать]
    elif sys.argv[1] == 'rollback':
        path_to_db = join_list(split_string(get_path_to_db()))
        k = split_string(path_to_db)[0:-1]
        k.append('{name}_backup.db'.format(name=split_string(path_to_db)[-1][0:len(split_string(path_to_db)[-1]) - 3]))
        path_to_backup = join_list(k)
        if len(sys.argv) == 3:
            path_to_backup = sys.argv[2]
        dbase.make_backup(path_to_backup, path_to_db)

    # argv содержит строку вида: main.exe sendall имя бота сообщение
    elif sys.argv[1] == 'sendall':
        if len(sys.argv) == 4:
            token = dbase.get_token(name=sys.argv[2])
            if token is None:
                print('Бот не найден')
            else:
                chats_id = dbase.get_all_chat_id(token=token)
                if chats_id is None:
                    print('Пользователи не найдены')
                elif sending_all(token, chats_id, sys.argv[3]) == 'ok':
                    print('Сообщение отправлено')
                else:
                    print('Произошла ошибка при отправке сообщений')

    else:
        # argv содержит строку вида: main.exe имя_бота Имя1 Имя2 ... сообщение, то совершить рассылку
        token = dbase.get_token(name=sys.argv[1])
        proxy_s = get_proxy()
        if token is None:
            print('Проверьте введенное имя бота')
        elif proxy_s == 'error':
            print('Введите прокси')
        elif len(sys.argv) < 4:
            print('Вы ввели недостаточно параметров')
        else:
            phones = sys.argv[2:len(sys.argv) - 1]
            message = sys.argv[len(sys.argv) - 1]

            sending(phones, message, token)
            print('Сообщение отправлено')
