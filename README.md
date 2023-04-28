# Telegram-Chess-Bot
[Телеграм-Бот](https://github.com/K1rL3s/Telegram-Chess-Bot) проект для Яндекс Лицея 2022/2023, работающий на 
[Шахматном API](https://github.com/K1rL3s/Simple-Chess-API). \
Бот позволяет играть в шахматы с движком [Stockfish](https://stockfishchess.org/) в [Telegram](https://telegram.org/). 

### Функционал
- Асинхронная работа за счёт библиотеки [aiogram](https://pypi.org/project/aiogram/)
- Интерфейс с помощью inline-кнопок
- Гибкая настройка уровня игры движка
- Кастомизация изображения доски
- Хранение информации о пользователе при помощи [sqlalchemy](https://pypi.org/project/SQLAlchemy/)
- Личная и глобальная статистика побед, поражений и ничьей
- Возможность получить подсказку и сдаться


### Запуск

1. Установить **python** версии **3.10**+
   (Тестировалось на версии **3.10.8**)

2. Склонировать репозиторий и перейти в него:

   ```
   git clone https://github.com/K1rL3s/Telegram-Chess-Bot.git
   cd ./Telegram-Chess-Bot
   ```

3. Создать и активировать виртуальное окружение:

   ```
   # Windows:
   python -m venv venv
   venv\Scripts\activate.bat
   
   # Linux:
   python3 -m venv venv
   source venv\Scripts\activate
   ```

4. Установить все нужные библиотеки. 

   ```
   pip install -r ./requirements.txt
   ```

5. Создать и заполнить файл `.env` в корневой папке (пример: `.env.example`):

   ```env
   CHESS_TG_TOKEN=<tg-bot-token>
   API_URL=http://ip:port/api/chess/
   API_AUTH_KEY=<token>
   LOG_CHAT=<chat-id>
   UPS=<int>
   CACHE_LIMIT_REQUEST=<int>
   CACHE_GLOBAL_TOP=<int>
   GLOBAL_TOP=<int>
   ```

6. Запустить бота:
   ```
   python ./main.py
   ```

### Скриншоты работы
![Telegram_WIFil9xgVJ](https://user-images.githubusercontent.com/104463209/233860960-e93ebf81-3e7d-4117-b385-7782fa9ec99e.png)
![Telegram_uX4z1D1z0H](https://user-images.githubusercontent.com/104463209/233860961-ab0b1102-d3d5-466c-9e19-581e13f3d0aa.png)
![Telegram_FaI7A4F93h](https://user-images.githubusercontent.com/104463209/233860963-3586a13a-91e7-495d-acb3-b827b365b685.png)
![chess_diagram](https://user-images.githubusercontent.com/104463209/233864355-bd1f823c-51c4-4b43-ac53-6a35112ca0fe.png)


### Пояснительная часть
Проект "Шахматный Телеграм Бот" был разработан Лесовым Кириллом по программе второго года Яндекс Лицея. \
Идея сделать бота возникла после создания шахматного API, которое использовалось на хакатоне ИТМО и Яндекса по созданию навыков для Алисы. \
Проект реализован при помощи асинхронной библиотеки aiogram, что позволило сделать такую интересную фичу, 
как "загружающееся сообщение" - те точки, которые обновляются в конце сообщения во время загрузки. \
Для всех вычислений и изображений используется шахматное API, про которое написано подробнее в нём самом.
