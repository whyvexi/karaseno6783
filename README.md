# 🎓 ExamPrep Bot — Telegram-бот для подготовки к экзаменам

Модульная архитектура на **aiogram 3.x + SQLAlchemy async + aiohttp**.

## Возможности

- **Онбординг**: выбор предмета (Python / SQL / Веб-разработка)
- **Тесты**: база вопросов с 4 вариантами ответов и подробными разборами
- **Лимиты**: 3 вопроса/день бесплатно; безлимит — с подпиской
- **Профиль**: статистика, стрик дней, статус подписки
- **3 провайдера оплаты**:
  - Telegram Stars (XTR) — нативные инвойсы
  - Platega.io — СБП / карты RUB
  - CryptoBot — USDT/TON

## Структура проекта

```
exam_bot/
├── config.py                  # Загрузка токенов из .env
├── constants.py               # Тарифы, предметы
├── main.py                    # Запуск бота + webhook-сервера
├── requirements.txt
├── .env.example
│
├── database/
│   ├── models.py              # Users, Subjects, Questions, Subscriptions, Payments, QuizAttempts
│   ├── database.py            # async engine + sessionmaker
│   └── seeds.py               # 6 тестовых вопросов (по 2 на предмет)
│
├── services/
│   ├── quiz_service.py        # Лимиты, выдача вопросов, рекорд попыток, статики
│   ├── subscription_service.py # activate_subscription (продление + идемпотентность)
│   └── payment_service.py     # PlategaClient, CryptoBotClient, создание Payment
│
├── handlers/
│   ├── start.py               # /start, онбординг, смена предмета
│   ├── quiz.py                # Прохождение тестов
│   ├── profile.py             # Профиль и статистика
│   └── payments.py            # Меню тарифов, выбор метода, pre_checkout, successful_payment
│
├── middlewares/
│   └── access.py              # DbSessionMiddleware (сессия + user + is_subscribed)
│
├── keyboards/
│   └── inline.py              # Все inline/reply клавиатуры
│
├── states/
│   └── quiz_states.py         # FSM states (Onboarding, Quiz)
│
└── webapp/
    └── webhook.py             # aiohttp-сервер для Platega/CryptoBot webhook
```

## Запуск

```bash
cd exam_bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Заполнить .env (скопировать из .env.example)
cp .env.example .env

python main.py
```

Бот запускается в режиме long-polling; webhook-сервер Platega/CryptoBot
поднимается на `WEBHOOK_PORT` (по умолчанию 8080).

## Тарифная сетка

| Тариф | Дни | RUB | Stars | USDT |
|-------|-----|-----|-------|------|
| Спринт | 7 | 199 | 130 | 2.2 |
| Месячный Pro | 30 | 499 | 320 | 5.5 |
| Семестр | 90 | 999 | 650 | 11.0 |

## Логика подписки

- `activate_subscription(user_id, plan_id, days, payment_id=...)`:
  - Если подписка активна — дни плюсуются к `ends_at`
  - Если истекла — отсчёт от `datetime.utcnow()`
  - **Идемпотентность**: повторный вызов с тем же `payment_id` возвращает `None`
