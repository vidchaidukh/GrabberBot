# GrabberBot
### Граббер(і парсер) програма для отримання нових оголошень на дошках у вигляді телеграм боту
Скористатися ботом можна за [посиланням](https://t.me/board_grabber_bot)
Тестове посилання - https://m.olx.ua/list/


_Автор:_ Михайлюк Євгеній, ІО-92<br>
_Пошта:_ mr.sapsan220@gmail.com<br>
_Телеграм:_ [Stupident](https://t.me/stupident)


#### Унікальність проекту:
При аналізі існуючих рішень мого завдання були знайдені бот оголошень з дошки auto.ria та бот olx-work. Вони побудовані на такій самій логіці, як і мій, працюють добре, але вузьконаправлені. Мій же проект зможе надавати доступ до багатьох дошок оголошень и моніторити багато пошукових запитів одночасно.


### Використання
Коли на дошку оголошень додається гарний, дешевий, крутий варіант, надовго він там не затримується. Його забирають за лічені хвилини. Це стосується не тільки речей, а й багато іншого: авто, квартири, навіть вакансії на роботу. Весь час сидіти на сайті неможливо фізично, а прогавити ідеальне оголошення легко.<br>
Саме з цією метою і була розроблена ця програма, яка з мінімальною затримкою відправить юзеру цікавляче його повідомлення у сучасний месенджер, який є майже у кожного.


#### Перший запуск <br>
![Перший запуск](https://github.com/Stupident/GrabberBot/blob/main/doc/start.gif)
#### Керування запитами <br>
![Керування запитами](https://github.com/Stupident/GrabberBot/blob/main/doc/delete.gif)
#### Нові оголошення <br>
![Нові оголошення](https://github.com/Stupident/GrabberBot/blob/main/doc/new_adv.gif)
#### Оповіщення  <br>
![Оповіщення](https://github.com/Stupident/GrabberBot/blob/main/doc/notification.gif)


#### Алгоритм роботи:
1) При першому запуску користувачем бота, дані користувача заносяться до таблиці users. 
2) Потім юзер може ініціювати пошуковий процес, просто відправивши посилання на сторінку з цікавлячими його товарами. 
3) Бот отримує посилання, аналізує його, визначає дошку оголошень та створює запис в таблицю requests.
4) Паралельно з ботом(bot.py) запущений процес перевірки нових оголошень (файл checker.py), котрий проходить по таблиці requests, витягає url та передає граберу відповідної дошки оголошень(*назва дошки*.py). 
5) Грабер завантажує html-код за вказаним url, потім парсер(написаний за допомогоб бібліотеки bs4) витягає необхідні дані. Якщо час створення оголошення не раніше останнього проходу checker-а, оголошення додається до таблиці adverts з міткою is_sended=false.
7) В боті також запущений 3-ій паралельний процес, що відповідає за відправку нових оголошень. Він кожен раз вибирає з таблиці adverts записи з міткою is_sended=false, конкатинує дані в повідомлення, відправляє та змінює мітку в БД на true.


#### Можливості для розширення:
Більшість дошок оголошень мають однакову конструкція і подібні параметри оголошення (Назва, ціна, місцезнаходження, фото та ціна). Тому буду не важко написати парсер для інших дошок, наприклад: izi.ua, auto.ria, dom.ria та навіть work.ua..
Також можна додати парсер всіх оголошень за посиланням з результатом у вигляді CSV-файлу або таблиці БД.


### Як був створений цей проект:
![Котик](https://media.giphy.com/media/aNqEFrYVnsS52/giphy.gif)
