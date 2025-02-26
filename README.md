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

2. Install system dependencies

```zsh
brew install tcl-tk@8
```

3. Create a virtual environment if there isn't one already

```zsh
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv
```

```zsh
/usr/local/opt/python@3.12/bin/python3.12 -m venv .venv
```

4. Activate virtual environment

```zsh
source .venv/bin/activate
```

5. Install project dependencies

```zsh
pip install -r requirements.txt
```

6. Install PaddlePaddle for PaddleOCR

```zsh
python -m pip install paddlepaddle==3.0.0b1 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

6. Run ReceiptLogger

```zsh
python -m app.main
```

### Google Sheets Authentication

1. Create a new project and enable Google Sheets API

2. Create a new service account for this project

3. Create a new json key for this service account

4. Ensure directory has .env with GOOGLE_KEY, SPREADSHEET_ID, and WORKSHEET_NAME

5. Give Editor access to client_email from .google_key.json on Google Sheet
