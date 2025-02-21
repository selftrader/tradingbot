from utils.data_loader import DataLoader

data_loader = DataLoader(source="yahoo")

# Fetch Index Data (NIFTY50)
index_data = data_loader.fetch_historical_data("NIFTY50", "2019-01-01", "2024-01-01", interval="1d", instrument_type="index")
data_loader.save_data_to_csv(index_data, "nifty50_data")

# Fetch Options Data (NIFTY Options)
options_data = data_loader.fetch_historical_data("NIFTY OPTIONS", "2022-01-01", "2024-01-01", interval="5m", instrument_type="options")
data_loader.save_data_to_csv(options_data, "nifty_options_data")

# Fetch Stock Data (Reliance)
stock_data = data_loader.fetch_historical_data("RELIANCE.NS", "2019-01-01", "2024-01-01", interval="1d", instrument_type="stocks")
data_loader.save_data_to_csv(stock_data, "reliance_data")

# Fetch Sectoral Data (NIFTY IT)
sectoral_data = data_loader.fetch_historical_data("NIFTY IT", "2020-01-01", "2024-01-01", interval="1d", instrument_type="sectoral")
data_loader.save_data_to_csv(sectoral_data, "nifty_it_data")
