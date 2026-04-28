## SHOM•AIR — интернет-магазин кроссовок, разработанный на Django.  

## Особенности проекта

- Django-проект с разделением на приложения
- Приложение `main` — основная логика сайта
- Приложение `cart` — корзина и работа с товарами
- Приложение `users` — регистрация, авторизация, профиль
- Приложение `orders` — Оформление заказов
- Приложение `payment` — платеж оформленных заказов
- Корзина покупок с контекстным процессором
- Система пользователей
- Шаблоны с наследованием
- Частичные шаблоны (partials)
- Поддержка static и media файлов
- Настройки через `.env`
- Работа проекта связана с `PostgreSQL` (База данных)

---

### Структура проекта

```
# Структура проекта Shom-Air

📂 shop/                    # Корневая директория проекта
├── 📂 cart/                # Приложение корзины
│   ├── 📂 migrations/
│   ├── 📂 templates/cart/
│   │   └── 📄 cart_detail.html
│   ├── 📄 __init__.py
│   ├── 📄 admin.py
│   ├── 📄 apps.py
│   ├── 📄 cart.py          # Логика корзины
│   ├── 📄 context_processors.py
│   ├── 📄 forms.py
│   ├── 📄 models.py
│   ├── 📄 tests.py
│   ├── 📄 urls.py
│   └── 📄 views.py
│
├── 📂 main/                # Основное приложение
│   ├── 📂 migrations/
│   ├── 📂 static/main/
│   │   ├── 📂 css/
│   │   │   └── 📄 style.css
│   │   └── 📂 js/
│   │       └── 📄 size-select.js
│   ├── 📂 templates/main/
│   │   ├── 📂 product/
│   │   │   ├── 📄 detail.html
│   │   │   └── 📄 list.html
│   │   └── 📄 base.html
│   ├── 📄 __init__.py
│   ├── 📄 admin.py
│   ├── 📄 apps.py
│   ├── 📄 models.py
│   ├── 📄 tests.py
│   ├── 📄 urls.py
│   └── 📄 views.py
│
├── 📂 media/               # медиа-файлы
│
├── 📂 orders/              # Приложение заказов
│   ├── 📂 migrations/
│   ├── 📂 templates/orders/
│   │   ├── 📂 partials/
│   │   │   └── 📄 summary.html
│   │   ├── 📄 checkout_content.html
│   │   ├── 📄 checkout.html
│   │   └── 📄 empty_cart.html
│   ├── 📄 __init__.py
│   ├── 📄 admin.py
│   ├── 📄 apps.py
│   ├── 📄 forms.py
│   ├── 📄 models.py
│   ├── 📄 tests.py
│   ├── 📄 urls.py
│   └── 📄 views.py
│
├── 📂 payment/             # Приложение оплаты (Stripe)
│   ├── 📂 migrations/
│   ├── 📂 templates/payment/
│   │   ├── 📄 stripe_cancel_content.html
│   │   ├── 📄 stripe_cancel.html
│   │   ├── 📄 stripe_success_content.html
│   │   └── 📄 stripe_success.html
│   ├── 📄 __init__.py
│   ├── 📄 admin.py
│   ├── 📄 apps.py
│   ├── 📄 models.py
│   ├── 📄 tests.py
│   ├── 📄 urls.py
│   └── 📄 views.py
│
├── 📂 shop/                # Директория конфигурации проекта
│   ├── 📄 __init__.py
│   ├── 📄 asgi.py
│   ├── 📄 settings.py
│   ├── 📄 urls.py
│   └── 📄 wsgi.py
│
├── 📂 users/               # Приложение пользователей
│   ├── 📂 migrations/
│   ├── 📂 templates/users/
│   │   ├── 📂 partials/
│   │   │   ├── 📄 account_details.html
│   │   │   └── 📄 edit_account_details.html
│   │   ├── 📄 base.html
│   │   ├── 📄 login.html
│   │   ├── 📄 profile.html
│   │   └── 📄 register.html
│   ├── 📄 __init__.py
│   ├── 📄 admin.py
│   ├── 📄 apps.py
│   ├── 📄 forms.py
│   ├── 📄 models.py
│   ├── 📄 tests.py
│   ├── 📄 urls.py
│   └── 📄 views.py
│
├── 📄 .env                 # Файл с секретными ключами
├── 📄 .env.example         # Пример структуры .env
├── 📄 .gitignore
├── 📄 manage.py            # Запуск проекта
├── 📄 README.md
└── 📄 requirements.txt     # Список зависимостей
```

---

# Запуск проекта:

### Клонирование репозитория

```
git clone https://github.com/muhammad-mirzoev/shom-air
cd shop
```

### Создание и активация виртуального окружения
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```
### Установка зависимостей
```
python -m pip install -r requirements.txt
```
```
Содержимое requirements.txt:
---
asgiref==3.11.0
certifi==2026.1.4
charset-normalizer==3.4.4
Django==6.0
idna==3.11
pillow==12.0.0
psycopg2==2.9.11
python-dotenv==1.2.1
requests==2.32.5
sqlparse==0.5.5
stripe==14.2.0
typing_extensions==4.15.0
urllib3==2.6.3
---
```

### Настройка переменных окружения Создайте файл .env (пример находится в .env.example):
Проект использует PostgreSQL (через psycopg2).
```
SECRET_KEY=
DEBUG=False

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```
### Применение миграций
```
python manage.py migrate
```
### Создание суперпользователя
```
python manage.py createsuperuser
```
# А после запуск
```
python manage.py runserver

Или:
python3 manage.py runserver
```

---

# 💳 Stripe найстройка 

Проект использует **Stripe** для обработки платежей. После клонирования репозитория необходимо выполнить следующие шаги. 

--- 

### 1. Создать аккаунт Stripe Если у вас ещё нет аккаунта: - Зарегистрируйтесь в Stripe - Перейдите в **Stripe Dashboard** - Убедитесь, что включён **Test mode** 


### 2. Получить Secret API Key В **Stripe Dashboard**: - Перейдите в **Developers → API keys** - Скопируйте Secret key (начинается с sk_) Добавьте его в переменные окружения:

```env
.env:

STRIPE_SECRET_KEY=your_stripe_secret_key_here

settings:

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
```

### 3. Установить и настроить Stripe CLI Проект использует **Stripe CLI** для работы с **webhooks** в локальной среде. 

**Установка Stripe CLI:** 

Инструкция для вашей ОС - https://stripe.com/docs/stripe-cli 

**Авторизация в Stripe:**
```
Выполните команду:

stripe login

Откроется терминал/консоль для авторизации в Stripe.
```

### 4. Запуск Webhook listener **Для получения webhook-событий от Stripe выполните команду:**
```
payment/views.py:

stripe listen --forward-to localhost:8000/payment/stripe/webhook/
```

**После запуска CLI выведет Webhook Signing Secret, например:**
```
your_stripe_webhook_secret_key_here
```

**Добавьте его в .env файл, а затем в settings.py:**
```
.env:

STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_key_here

settings.py:

STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
```
### В итоге у вас должно быть вот так:
```
settings.py:

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

.env -> ваш ключ:
например:

STRIPE_SECRET_KEY=your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_key_here
```

### 5. Запуск проекта **После настройки переменных окружения и запуска webhook listener можно запускать приложение:**
```
пример в терминале 
npm run dev

# или
python manage.py runserver

(используйте команду запуска, соответствующую вашему)
```