# PayCheck

A production-quality work schedule and payslip tracking web application built with Flask, MySQL, and Docker.

> Built as an internal tool and portfolio project to track shifts across multiple jobs, import calendar data, and estimate monthly net pay using Swedish tax rules.

---

## Screenshots
Coming Soon! 

---

## Features

- **User authentication** — Secure email/password login with bcrypt password hashing and CSRF protection
- **Multi-job support** — Create and manage multiple jobs, each with their own hourly rate and currency
- **Shift tracking** — Log shifts manually or import them from `.ics` calendar files
- **Recurring event support** — ICS imports correctly expand recurring events up to one year ahead
- **Calendar feed subscriptions** — Paste a live ICS URL and keep shifts automatically in sync
- **Auto-sync** — Calendar feeds sync automatically in the background every hour via APScheduler
- **OB supplement (obekväm arbetstid)** — Define custom OB rules per job with user-defined time windows and percentage bonuses for evenings, nights, weekends, and public holidays
- **Payslip estimation** — Monthly payslip calculator with full Swedish tax breakdown including grundavdrag, municipal tax, state tax, and OB supplements
- **Swedish public holidays** — Automatically recognised via `workalendar`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask 3.0 |
| Database | MySQL 8.0, SQLAlchemy ORM, Flask-Migrate |
| Auth | Flask-Login, Flask-Bcrypt, Flask-WTF (CSRF) |
| Calendar | icalendar, recurring-ical-events |
| Scheduling | APScheduler |
| Tax & Holidays | Custom Swedish tax engine, workalendar |
| Frontend | Jinja2, Bootstrap 5, Bootstrap Icons |
| Infrastructure | Docker, Docker Compose |

---

## Setup & Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/paycheck.git
cd paycheck
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
FLASK_ENV=development
SECRET_KEY=your-long-random-secret-key
DB_USER=worktrack
DB_PASSWORD=your-db-password
DB_ROOT_PASSWORD=your-root-password
DB_HOST=db
DB_NAME=worktrack
```

### 3. Build and start the containers

```bash
docker compose up --build
```

### 4. Run database migrations

```bash
docker compose exec web flask db upgrade
```

### 5. Open the app

Visit [http://localhost:5000](http://localhost:5000) and register an account.

---

### Development

To run with live reload (Docker Watch):

```bash
docker compose watch
```

Changes to the `app/` directory will sync instantly without restarting the container.

---

## Environment Variables

| Variable | Description |
|---|---|
| `FLASK_ENV` | `development` or `production` |
| `SECRET_KEY` | Flask secret key for session signing |
| `DB_USER` | MySQL username |
| `DB_PASSWORD` | MySQL password |
| `DB_ROOT_PASSWORD` | MySQL root password |
| `DB_HOST` | Database host (use `db` for Docker) |
| `DB_NAME` | Database name |
