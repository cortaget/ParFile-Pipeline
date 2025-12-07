# SOC API - Competition Management System

[Čeština](#česká-verze) | [English](#english-version) | [Русский](#русская-версия)

---

## English Version

### Project Structure

```
project/
│
├── app.py              # Main application file
├── data.py             # Data storage (global variables)
├── auth.py             # Authentication module (login, logout)
├── users.py            # User management
├── submissions.py      # Submissions management
├── rounds.py           # Rounds management
├── participants.py     # Participants management
├── ratings.py          # Ratings and downloads
├── results.py          # Results and publishing
└── reports.py          # Report generation
```

### Module Descriptions

#### app.py
Main file that:
- Creates Flask application
- Registers all blueprints
- Contains homepage

#### data.py
Centralized data storage:
- `users` - users dictionary
- `submissions` - submissions dictionary
- `sessions` - session tokens
- `rounds` - competition rounds
- `participants` - round participants
- `ratings` - submission ratings
- `results` - round results
- `reports` - generated reports

#### auth.py
Authentication:
- `/restapi/v1/login` - user login
- `/restapi/v1/logout` - user logout
- `get_current_user()` - function to get current user

#### users.py
User management:
- `POST /restapi/v1/users` - user registration
- `GET /restapi/v1/users` - list all users
- `GET /restapi/v1/me` - current user info

#### submissions.py
Submission management:
- `POST /restapi/v1/submissions` - create submission
- `GET /restapi/v1/submissions` - list submissions
- `PUT /restapi/v1/submissions/<id>` - update submission
- `DELETE /restapi/v1/submissions/<id>` - delete submission

#### rounds.py
Round management (organizer only):
- `POST /restapi/v1/rounds` - create round
- `GET /restapi/v1/rounds` - list rounds
- `GET /restapi/v1/rounds/<id>` - get round
- `PUT /restapi/v1/rounds/<id>` - update round
- `DELETE /restapi/v1/rounds/<id>` - delete round

#### participants.py
Participant management (organizer only):
- `POST /restapi/v1/rounds/<id>/participants` - add participant
- `GET /restapi/v1/rounds/<id>/participants` - list participants
- `PUT /restapi/v1/rounds/<id>/participants/<user_id>` - update participant
- `DELETE /restapi/v1/rounds/<id>/participants/<user_id>` - remove participant

#### ratings.py
Ratings (judge only):
- `POST /restapi/v1/submissions/<id>/ratings` - rate submission
- `GET /restapi/v1/submissions/<id>/ratings` - get ratings
- `GET /restapi/v1/rounds/<id>/submissions/pdf` - download submissions as PDF

#### results.py
Results:
- `GET /restapi/v1/rounds/<id>/results` - calculate results
- `POST /restapi/v1/rounds/<id>/publish` - publish results (organizer only)
- `GET /restapi/v1/public/results` - public results

#### reports.py
Reports (organizer and admin only):
- `GET /restapi/v1/rounds/<id>/report?format=pdf` - generate report

### Installation & Run

```bash
# Install dependencies
pip install flask

# Run server
python app.py
```

Server will start on `http://0.0.0.0:80`

### User Roles

- `soutezici` - competitors (create submissions)
- `porotce` - judges (rate submissions)
- `poradatel` - organizers (manage rounds)
- `admin` - administrators (access to reports)

### API Examples

#### Register User
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Martin","email":"martin@example.com","role":"soutezici","password":"123"}'
```

#### Login
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/login \
  -H "Content-Type: application/json" \
  -d '{"name":"Martin","password":"123"}'
```

#### Create Submission
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"My Project"}'
```

---

## Česká Verze

### Struktura Projektu

```
project/
│
├── app.py              # Hlavní soubor aplikace
├── data.py             # Úložiště dat (globální proměnné)
├── auth.py             # Modul autentizace (přihlášení, odhlášení)
├── users.py            # Správa uživatelů
├── submissions.py      # Správa soutěžních prací
├── rounds.py           # Správa kol
├── participants.py     # Správa účastníků
├── ratings.py          # Hodnocení a stahování
├── results.py          # Výsledky a zveřejnění
└── reports.py          # Generování reportů
```

### Popis Modulů

#### app.py
Hlavní soubor, který:
- Vytváří Flask aplikaci
- Registruje všechny blueprinty
- Obsahuje domovskou stránku

#### data.py
Centralizované úložiště dat:
- `users` - slovník uživatelů
- `submissions` - slovník prací
- `sessions` - tokeny relací
- `rounds` - soutěžní kola
- `participants` - účastníci kol
- `ratings` - hodnocení prací
- `results` - výsledky kol
- `reports` - vygenerované reporty

#### auth.py
Autentizace:
- `/restapi/v1/login` - přihlášení uživatele
- `/restapi/v1/logout` - odhlášení uživatele
- `get_current_user()` - funkce pro získání aktuálního uživatele

#### users.py
Správa uživatelů:
- `POST /restapi/v1/users` - registrace uživatele
- `GET /restapi/v1/users` - seznam všech uživatelů
- `GET /restapi/v1/me` - informace o aktuálním uživateli

#### submissions.py
Správa prací:
- `POST /restapi/v1/submissions` - vytvoření práce
- `GET /restapi/v1/submissions` - seznam prací
- `PUT /restapi/v1/submissions/<id>` - úprava práce
- `DELETE /restapi/v1/submissions/<id>` - smazání práce

#### rounds.py
Správa kol (pouze pro pořadatele):
- `POST /restapi/v1/rounds` - vytvoření kola
- `GET /restapi/v1/rounds` - seznam kol
- `GET /restapi/v1/rounds/<id>` - získání kola
- `PUT /restapi/v1/rounds/<id>` - úprava kola
- `DELETE /restapi/v1/rounds/<id>` - smazání kola

#### participants.py
Správa účastníků (pouze pro pořadatele):
- `POST /restapi/v1/rounds/<id>/participants` - přidání účastníka
- `GET /restapi/v1/rounds/<id>/participants` - seznam účastníků
- `PUT /restapi/v1/rounds/<id>/participants/<user_id>` - úprava účastníka
- `DELETE /restapi/v1/rounds/<id>/participants/<user_id>` - odebrání účastníka

#### ratings.py
Hodnocení (pouze pro porotce):
- `POST /restapi/v1/submissions/<id>/ratings` - ohodnocení práce
- `GET /restapi/v1/submissions/<id>/ratings` - získání hodnocení
- `GET /restapi/v1/rounds/<id>/submissions/pdf` - stažení prací jako PDF

#### results.py
Výsledky:
- `GET /restapi/v1/rounds/<id>/results` - výpočet výsledků
- `POST /restapi/v1/rounds/<id>/publish` - zveřejnění výsledků (pouze pořadatel)
- `GET /restapi/v1/public/results` - veřejné výsledky

#### reports.py
Reporty (pouze pro pořadatele a administrátory):
- `GET /restapi/v1/rounds/<id>/report?format=pdf` - generování reportu

### Instalace & Spuštění

```bash
# Instalace závislostí
pip install flask

# Spuštění serveru
python app.py
```

Server se spustí na `http://0.0.0.0:80`

### Role Uživatelů

- `soutezici` - soutěžící (vytvářejí práce)
- `porotce` - rozhodčí (hodnotí práce)
- `poradatel` - pořadatelé (spravují kola)
- `admin` - administrátoři (přístup k reportům)

### Příklady API

#### Registrace Uživatele
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Martin","email":"martin@example.com","role":"soutezici","password":"123"}'
```

#### Přihlášení
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/login \
  -H "Content-Type: application/json" \
  -d '{"name":"Martin","password":"123"}'
```

#### Vytvoření Práce
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"Můj Projekt"}'
```

---

## Русская Версия

### Структура Проекта

```
project/
│
├── app.py              # Главный файл приложения
├── data.py             # Хранилище данных (глобальные переменные)
├── auth.py             # Модуль аутентификации (вход, выход)
├── users.py            # Управление пользователями
├── submissions.py      # Управление работами
├── rounds.py           # Управление раундами
├── participants.py     # Управление участниками
├── ratings.py          # Оценки и загрузки
├── results.py          # Результаты и публикация
└── reports.py          # Генерация отчетов
```

### Описание Модулей

#### app.py
Главный файл, который:
- Создает Flask приложение
- Регистрирует все blueprints
- Содержит домашнюю страницу

#### data.py
Централизованное хранилище данных:
- `users` - словарь пользователей
- `submissions` - словарь работ
- `sessions` - токены сессий
- `rounds` - раунды соревнований
- `participants` - участники раундов
- `ratings` - оценки работ
- `results` - результаты раундов
- `reports` - сгенерированные отчеты

#### auth.py
Аутентификация:
- `/restapi/v1/login` - вход пользователя
- `/restapi/v1/logout` - выход пользователя
- `get_current_user()` - функция получения текущего пользователя

#### users.py
Управление пользователями:
- `POST /restapi/v1/users` - регистрация пользователя
- `GET /restapi/v1/users` - список всех пользователей
- `GET /restapi/v1/me` - информация о текущем пользователе

#### submissions.py
Управление работами:
- `POST /restapi/v1/submissions` - создание работы
- `GET /restapi/v1/submissions` - список работ
- `PUT /restapi/v1/submissions/<id>` - обновление работы
- `DELETE /restapi/v1/submissions/<id>` - удаление работы

#### rounds.py
Управление раундами (только для организаторов):
- `POST /restapi/v1/rounds` - создание раунда
- `GET /restapi/v1/rounds` - список раундов
- `GET /restapi/v1/rounds/<id>` - получение раунда
- `PUT /restapi/v1/rounds/<id>` - обновление раунда
- `DELETE /restapi/v1/rounds/<id>` - удаление раунда

#### participants.py
Управление участниками (только для организаторов):
- `POST /restapi/v1/rounds/<id>/participants` - добавить участника
- `GET /restapi/v1/rounds/<id>/participants` - список участников
- `PUT /restapi/v1/rounds/<id>/participants/<user_id>` - обновить участника
- `DELETE /restapi/v1/rounds/<id>/participants/<user_id>` - удалить участника

#### ratings.py
Оценки (только для судей):
- `POST /restapi/v1/submissions/<id>/ratings` - оценить работу
- `GET /restapi/v1/submissions/<id>/ratings` - получить оценки
- `GET /restapi/v1/rounds/<id>/submissions/pdf` - скачать работы в PDF

#### results.py
Результаты:
- `GET /restapi/v1/rounds/<id>/results` - вычислить результаты
- `POST /restapi/v1/rounds/<id>/publish` - опубликовать результаты (только организатор)
- `GET /restapi/v1/public/results` - публичные результаты

#### reports.py
Отчеты (только для организаторов и администраторов):
- `GET /restapi/v1/rounds/<id>/report?format=pdf` - сгенерировать отчет

### Установка и Запуск

```bash
# Установка зависимостей
pip install flask

# Запуск сервера
python app.py
```

Сервер запустится на `http://0.0.0.0:80`

### Роли Пользователей

- `soutezici` - участники (создают работы)
- `porotce` - судьи (оценивают работы)
- `poradatel` - организаторы (управляют раундами)
- `admin` - администраторы (доступ к отчетам)

### Примеры API

#### Регистрация Пользователя
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Martin","email":"martin@example.com","role":"soutezici","password":"123"}'
```

#### Вход
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/login \
  -H "Content-Type: application/json" \
  -d '{"name":"Martin","password":"123"}'
```

#### Создание Работы
```bash
curl -X POST http://127.0.0.1:80/restapi/v1/submissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"Мой Проект"}'
```

---

## License

MIT License

## Author

SOC Competition Management System