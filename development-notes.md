### Key principles

* Routes handle only http concerns. All buisness logic lives in services.py 
* Timezone rule: always store UTC in db, convert to user timezone at display time. iclander events carry tzinfo - normalise with pytz or zoneinfo

### Project main structure
worktrack/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # db, login_manager, csrf, bcrypt instances
│   ├── config.py                # Config classes (Dev/Prod/Test)
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── services.py          # register, login logic
│   │
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── services.py
│   │
│   ├── shifts/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   ├── services.py          # shift CRUD, dedup logic
│   │   └── ics_parser.py        # calendar import logic
│   │
│   ├── payslips/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── services.py          # aggregation, calls tax engine
│   │   └── tax/
│   │       ├── __init__.py
│   │       ├── base.py          # Abstract TaxStrategy
│   │       ├── uk_paye.py       # Concrete implementation
│   │       └── flat_rate.py     # Simple alternative
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── job.py
│   │   ├── shift.py
│   │   └── payslip.py
│   │
│   └── templates/
│       ├── base.html
│       ├── auth/
│       ├── jobs/
│       ├── shifts/
│       └── payslips/
│
├── migrations/                  # Flask-Migrate (Alembic)
├── tests/
├── docker/
│   ├── flask/Dockerfile
│   └── mysql/init.sql
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── run.py