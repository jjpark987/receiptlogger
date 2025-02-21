# ReceiptLogger

This repository contains the model, API, and UI for ReceiptLogger.

## Getting Started

### Prerequisites

- Python 3.12.9

### Installation

1. Clone the repository

```zsh
git clone git@github.com:jjpark987/receiptlogger.git
```

2. Create a virtual environment if there isn't one already

```zsh
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv
```

3. Activate virtual environment

```zsh
source .venv/bin/activate
```

4. Install dependencies

```zsh
pip install -r requirements.txt
```

5. Install paddlepaddle

```zsh
python -m pip install paddlepaddle==3.0.0b1 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

5. Run API server

```zsh
uvicorn app.main:app --host 0.0.0.0 --port 80
```

The API should now be running at http://0.0.0.0:80.

6. Run Tkinter NEED BREW TCL-TK!!!!!!!!!!

```zsh
python -m app.tk
```



<!-- ## Alebmic Version Control

This project uses Alembic for managing database migrations and version control. Whenever there are updates to the database models, we must create and apply a migration to ensure that the database schema remains in sync with the application’s data structures.

1. Create migration

```zsh
alembic revision --autogenerate -m "Migration message"
```

2. Migrate

```zsh
alembic upgrade head
```

## Seeding Database

To seed the database with:
- 3 categories (data manipulations, combinatorics, optimizations)
- subcategories for each category

- Make sure MySQL database server is up and migrated with the latest migration

- Seed database

```zsh
python -m app.seed
```

## Docker

### Commands

- Build image and create container in the foreground

```zsh
docker compose up --build
```

- List all containers

```zsh
docker ps -a
```

- Prune all stopped containers

```zsh
docker container prune -f
``` -->