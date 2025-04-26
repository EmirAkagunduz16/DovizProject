# USD to TRY Exchange Rate Tracker

This project tracks USD to TRY exchange rates in real-time, stores them in a PostgreSQL database, and visualizes them using Grafana.

## Setup

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Start the Docker containers:

```bash
docker-compose up -d
```

3. Run the data collection script:

```bash
python save_database.py
```

## Accessing the Services

- PostgreSQL:
  - Host: localhost
  - Port: 5432
  - Database: doviz
  - Username: postgres
  - Password: postgres

- Grafana:
  - URL: http://localhost:3000
  - Username: admin
  - Password: admin

## Setting up Grafana

1. Log in to Grafana at http://localhost:3000
2. Add PostgreSQL as a data source:
   - Type: PostgreSQL
   - Host: postgres:5432 (important: use 'postgres' not 'localhost')
   - Database: doviz
   - User: postgres
   - Password: postgres
   - SSL Mode: Disable
3. Click "Save & Test" to verify the connection
4. Create a new dashboard and add a time series panel
5. Use this SQL query for the panel:

```sql
SELECT
  timestamp as time,
  usd_to_try_rate as value
FROM exchange_rates
ORDER BY timestamp
```
"# DovizProject" 
