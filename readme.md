# Booking Service

Сервис бронирования, созданный с помощью Python и Django (DRF).

## Установка

```bash
git clone <repository-url>
cd booking-service
```

## Конфигурация

Скопируйте файл среды `.env.example` и настройте параметры:

```env
DJANGO_SECRET_KEY="secret-key"
DJANGO_DEBUG=True
DB_NAME=booking_service
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

Отредактируйте  файл `.env`, указав свои настройки.

### Запуск с помощью Docker Compose

Соберите и запустите сервис с помощью Docker Compose:

```bash
docker-compose up --build
```

Чтобы остановить сервис, используйте:

```bash
docker-compose down
```

### Запуск локально

Инициализируйте виртуальную среду:

```bash
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate
```

Инициализируйте зависимости:

```bash
pip install -r requirements.txt
```

Мигрируйте базу данных:

```bash
python manage.py migrate
```

Запустите сервис:

```bash
python manage.py runserver
```

Или запустить с Gunicorn для продакшна:

```bash
gunicorn --bind 0.0.0.0:8000 booking_service.wsgi:application 
```

## API Документация

Сервис предоставляет REST API

Полная документация в Swagger:

```
http://localhost:8000/api/schema/swagger-ui/
```

или ReDoc:

```
http://localhost:8000/api/schema/redoc/
```