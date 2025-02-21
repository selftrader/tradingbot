# Trading Bot

A full-stack trading bot application for configuring broker accounts, monitoring live market data, and automating trading sessions. This repository contains both a Python backend (using FastAPI) and a React/Material‑UI frontend.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication:** Login and signup with user-specific configurations.
- **Broker Account Management:** Add, edit, delete and activate/deactivate broker configurations.
- **Live Updates:** Real-time market data display and live trading status.
- **Trading Sessions:** Start and stop bot sessions, monitor trades.
- **Dark Mode UI:** Consistent dark-themed interface built with Material‑UI.

## Tech Stack

- **Frontend:** React, Material‑UI, React Router
- **Backend:** Python, FastAPI, SQLAlchemy (with PostgreSQL or SQLite)
- **Version Control:** Git with Git LFS for asset storage (if needed)

## Installation

### Prerequisites

- Node.js (v14+)
- Python 3.8+
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd /path/to/tradingapp-main/tradingapp-main
```

## Folder Structure

trading_bot_ai/ ├── README.md ├── requirements.txt ├── config.py ├── global_state.py ├── main.py ├── data/ │ └── sample_data.csv ├── logs/ │ └── bot.log ├── models/ │ ├── init.py │ ├── predictor.py │ └── learning_module.py ├── broker/ │ ├── init.py │ ├── base_broker.py │ ├── dhan_api.py │ └── multi_broker_api.py ├── strategies/ │ ├── init.py │ └── strategy.py ├── ui/ │ ├── app.py │ └── templates/ │ └── index.html ├── utils/ │ ├── init.py │ ├── logger.py │ ├── data_loader.py │ └── trade_history.py └── tests/ └── test_strategy.py