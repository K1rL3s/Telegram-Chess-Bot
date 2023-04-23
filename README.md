# Telegram-Chess-Bot
[Телеграм-Бот](https://github.com/K1rL3s/Telegram-Chess-Bot) проект для Яндекс Лицея 2022/2023, работающий на 
[Шахматном API](https://github.com/K1rL3s/Simple-Chess-API). \
Бот позволяет играть в шахматы с движком [Stockfish](https://stockfishchess.org/) в [Telegram](https://telegram.org/). 

### Функционал
- Асинхронная работа за счёт библиотеки [aiogram](https://pypi.org/project/aiogram/)
- Интерфейс с помощью inline-кнопок
- Гибкая настройка уровня игры движка
- Кастомизация изображения доски
- Личная и глобальная статистика побед, поражений и ничьей
- Возможность получить подсказку и сдаться


### Запуск

1. Установить **python** версии **3.10**+
   (Тестировалось на версии **3.10.8**)

2. Склонировать репозиторий и перейти в него:

```commandline
git clone https://github.com/K1rL3s/Telegram-Chess-Bot.git
cd ./Telegram-Chess-Bot
```

3. Создать и активировать виртуальное окружение:

```commandline
# Windows:
python -m venv venv
venv\Scripts\activate.bat

# Linux:
python3 -m venv venv
source venv\Scripts\activate
```

4. Установить все нужные библиотеки. 

```commandline
pip install -r ./requirements.txt
```

5. Создать и заполнить файл `.env` в корневой папке (пример: `.env.example`):

```env
CHESS_TG_TOKEN=<tg-bot-token>
API_URL=http://ip:port/api/chess/
API_AUTH_KEY=<token>
LOG_CHAT=<chat-id>
```

6. Запустить бота:

```commandline
python ./main.py
```

### Скриншоты работы
...


### Пояснительная часть
Проект "Шахматный Телеграм Бот" был разработан Лесовым Кириллом по программе второго года Яндекс Лицея. \
Идея сделать бота возникла после создания шахматного API, которое использовалось на хакатоне ИТМО и Яндекса по созданию навыков для Алисы. \
Проект реализован при помощи асинхронной библиотеки aiogram, что позволило сделать такую интересную фичу, 
как "загружающееся сообщение" - те точки, которые обновляются в конце сообщения во время загрузки. \
Для всех вычислений и изображений используется шахматное API, про которое написано подробнее в нём самом.
