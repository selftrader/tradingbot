# Autonomous Trading Bot for Indian Share Market

This project implements a production‑ready autonomous trading bot that:
- Uses a pre‑trained AI predictor combined with technical analysis (moving averages) to generate trading signals.
- Executes trades via a DHAN API integration (expandable to multi‑broker support).
- Records trade outcomes and updates the model using a learning module.
- Provides a real‑time dashboard using Flask‑SocketIO.

## Folder Structure

trading_bot_ai/ ├── README.md ├── requirements.txt ├── config.py ├── global_state.py ├── main.py ├── data/ │ └── sample_data.csv ├── logs/ │ └── bot.log ├── models/ │ ├── init.py │ ├── predictor.py │ └── learning_module.py ├── broker/ │ ├── init.py │ ├── base_broker.py │ ├── dhan_api.py │ └── multi_broker_api.py ├── strategies/ │ ├── init.py │ └── strategy.py ├── ui/ │ ├── app.py │ └── templates/ │ └── index.html ├── utils/ │ ├── init.py │ ├── logger.py │ ├── data_loader.py │ └── trade_history.py └── tests/ └── test_strategy.py