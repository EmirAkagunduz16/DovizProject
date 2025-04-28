# Doviz Project - USD/TRY Exchange Rate Monitor

This project monitors USD/TRY exchange rates in real-time using InfluxDB for data storage and Grafana for visualization.

## Features

- Real-time USD/TRY exchange rate monitoring
- Data storage in InfluxDB
- Beautiful visualizations with Grafana
- Docker-based deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`)

## Project Structure

```
DovizProject/
├── docker-compose.yml    # Docker configuration for InfluxDB and Grafana
├── save_database.py      # Python script to fetch and save exchange rates
└── README.md            # This file
```

## Setup Instructions

1. **Start Docker Containers**
   ```bash
   docker-compose up -d
   ```

2. **Access Services**
   - InfluxDB UI: http://localhost:8087
     - Username: emiraka
     - Password: emir16gs
   - Grafana: http://localhost:3000
     - Username: admin
     - Password: admin123

3. **Configure Grafana Data Source**
   - Go to Configuration → Data Sources
   - Add InfluxDB data source with:
     - URL: http://influxdb:8086
     - Organization: MyWork
     - Bucket: exchange_rates
     - Token: (your InfluxDB token)

4. **Run the Python Script**
   ```bash
   python save_database.py
   ```

## Creating a Dashboard in Grafana

1. Click "+" → New dashboard
2. Add visualization
3. Choose Time series
4. Configure query:
   - From: exchange_rates
   - Measurement: usd_to_try
   - Field: rate

## Troubleshooting

### Common Issues

1. **Grafana can't connect to InfluxDB**
   - Verify the URL in Grafana data source is `http://influxdb:8086`
   - Check if both containers are running: `docker ps`

2. **Permission Errors**
   - Ensure your InfluxDB token has read/write permissions
   - Verify organization name matches in both InfluxDB and Grafana

3. **Port Conflicts**
   - Check if ports 3000 (Grafana) and 8087 (InfluxDB) are available
   - Modify ports in docker-compose.yml if needed

## API Information

This project uses the Open Exchange Rates API to fetch USD/TRY exchange rates. The API is free to use and doesn't require an API key.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License.
