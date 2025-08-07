# 🌌 Void-Connect
## Асинхронный **Telegram бот** для продажи и управления **VPN подписками**.  
- Взаимодействие с ботом через **Inline-кнопки** 
- Интеграция с панелью [**3x-ui**](https://github.com/MHSanaei/3x-ui) с использованием библиотеки [**py3xui**](https://github.com/iwatkot/py3xui)  
- Хранение данных пользователей в **PostgreSQL** с применением **SQLAlchemy** для взаимодействия  
- Логирование транзакций и ошибок в **Telegram супергруппу**  
- Поддержка оплаты в **рублях** через **YooKassa** и в **Telegram Stars** ⭐
## 🧰 Использованный стек технологий
- python 3.11
  - aiogram 3.17
  - python-dotenv 1.1.0
  - py3xui
  - SQLAlchemy
  - yookassa
- PostgreSQL 17
## Сущности базы данных
- users (Пользователи)
- transactions (Транзакции)
- promo (Промокоды)

