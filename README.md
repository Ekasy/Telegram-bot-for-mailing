# Telegram-bot-for-mailing
The application was created for convenient distribution of information in the Telegram.

Для работы с приложением для начала необходимо скачать исходники и разместить их на компьютере.
Создать и активировать виртуальное окружение, и командой <code>pip3 install -r requirements.txt</code> установить необходимые библиотеки.
Зарегестрировать своего бота в Telegram, написав BotFather, и, следуя его инструкциям, получить токен.

В файле db/settings.json записаны имя и путь к базе данных и прокси. Данную информацию можно забить сразу в файл, либо запустить файл db/settings.py с или без параметров.

Все приготовления закончены. Следующим шагом станет запуск бота через приложение для набора массы пользователей. Ниже приведены команды работы приложения:

<code>main.exe start your_token file1.json</code> - данной командой происходит запуск бота, где
<br>start - параметр запуска
<br>your_token - токен вашего бота
<br>file1.json - имя файла в котором содержатся фразы используемые ботом для ответа на различные действия пользователя. Файл можно редактировать, 
вводя свои фразы.

<code>main.exe stop bot_name</code> - данной командой происходит остановка бота
<br>bot_name - имя бота, которые вы задали BotFather (без добавки "bot")

<code>main.exe bot_name name1 [name2] "Hello!"</code> - отправка сообщения <em>Hello!</em> введеным пользователям

<code>main.exe sendall bot_name "Hello everybody!"</code> - отправка сообщения <em>Hello everybody!</em> всем пользователям через бота <strong>bot_name</strong>

<code>main.exe backup [path_to_bd]</code> - создание копии базы данных
<br>path_to_bd - необязательный параметр, путь к месту, где будет храниться копия базы данных

<code>main.exe rollback [path_to_bd]</code> - откат текущей бд к версии сохраненной копии
<br>path_to_bd - необязательный параметр, путь к месту, где храниться копия базы данных

# Немного о приложении
Приложение разработано таким образом, чтобы на одном устройстве можно было запускать несколько ботов одновременно.
Они все корректно общаются с базой данных и не мешают друг другу. Само приложение бота запускается в фоновом режиме. 
Важно завершать работу бота командой, иначе информация о работе бота не обновиться и программа посчитает, что бот уже запущен, 
решается остановкой бота.

Рассылку сообщений можно производить как включенным, так и остановленным ботом. Работающий бот только регистрирует новых пользователей, записывая их в базу данных.

Разработка завершилась до того, как РКН разблокировал Telegram на территории РФ, поэтому используется прокси, который был найден на просторах сети)

Написано на python 3.8, поддерживается на Windows и Ubuntu.