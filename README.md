# Exchange Rate Tracker using InfluxDB

This project fetches USD to TRY exchange rates and stores them in an InfluxDB database.

## Prerequisites

- Python 3.6+
- InfluxDB (version 1.x)
- yfinance library
- influxdb library (Python client for InfluxDB 1.x)
- pandas library

## Setup Instructions

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Setup InfluxDB 1.x:
   - Download and install InfluxDB 1.x from https://portal.influxdata.com/downloads/
   - Extract the downloaded zip to a location of your choice (e.g., `C:\Users\Victus\influxdb`)
   - Navigate to the extracted directory and run InfluxDB:
     ```
     cd C:\Users\Victus\influxdb\influxdb-1.11.8-1
     .\influxd.exe
     ```

3. (Optional) Configure InfluxDB credentials:
   - By default, InfluxDB 1.x runs without authentication enabled
   - If you've set up authentication, update the following variables in both `save_database.py` and `query_data.py`:
     ```python
     INFLUXDB_USER = "your_username"
     INFLUXDB_PASS = "your_password"
     ```

## Running the Application

1. Start InfluxDB:
   ```
   cd C:\Users\Victus\influxdb\influxdb-1.11.8-1
   .\influxd.exe
   ```

2. In another terminal, run the application:
   ```
   python save_database.py
   ```

The application will:
1. Connect to InfluxDB and create a database called "exchange_rates" if it doesn't exist
2. Fetch the USD to TRY exchange rate every 30 seconds
3. Store each rate in the InfluxDB database with a timestamp

## Querying Data

To query the stored data, run:
```
python query_data.py
```

This script will:
1. Connect to the InfluxDB database
2. Retrieve exchange rate data from the past 24 hours
3. Display statistics and the last 10 records

You can also interact directly with InfluxDB using the InfluxDB CLI:
```
cd C:\Users\Victus\influxdb\influxdb-1.11.8-1
.\influx.exe
```

Then in the InfluxDB shell:
```
USE exchange_rates
SELECT * FROM usd_to_try ORDER BY time DESC LIMIT 10
```
