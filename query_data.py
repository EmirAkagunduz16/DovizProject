from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta
import pandas as pd

# InfluxDB connection parameters - match save_database.py
INFLUXDB_URL = "http://localhost:8087"
INFLUXDB_TOKEN = "CUuxTbAY5jhbhL3RV8HUPJNAXC9P_1ZjQ5hzMK05nKR3iFl8vWF8ESLrkS7IYu7_nEU1yOY6Qvx6xqQ2wU1R7A=="
INFLUXDB_ORG = "MyWork"
INFLUXDB_BUCKET = "exchange_rates"

def query_exchange_rates(hours=24):
    """Query exchange rates for the last specified hours"""
    try:
        # Create a client connection to InfluxDB with token authentication
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        
        # Prepare time range for query
        time_now = datetime.utcnow()
        time_from = time_now - timedelta(hours=hours)
        
        # Flux query (used in InfluxDB 2.x)
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
            |> range(start: -{hours}h)
            |> filter(fn: (r) => r._measurement == "usd_to_try")
            |> filter(fn: (r) => r._field == "rate")
        '''
        
        # Execute the query
        result = client.query_api().query_data_frame(query=query, org=INFLUXDB_ORG)
        client.close()
        
        # Check if result is empty
        if result is None or len(result) == 0:
            print("No data found")
            return None
            
        # Process the DataFrame
        result_df = result.copy()
        
        # Process the result for display
        print(f"Retrieved {len(result_df)} records from the past {hours} hours")
        
        # Display the results
        display_df = pd.DataFrame({
            'Time': result_df['_time'],
            'USD/TRY Rate': result_df['_value']
        })
        
        # Calculate statistics
        if not display_df.empty:
            min_rate = display_df['USD/TRY Rate'].min()
            max_rate = display_df['USD/TRY Rate'].max()
            avg_rate = display_df['USD/TRY Rate'].mean()
            
            print(f"\nStatistics for the past {hours} hours:")
            print(f"Minimum Rate: {min_rate:.4f}")
            print(f"Maximum Rate: {max_rate:.4f}")
            print(f"Average Rate: {avg_rate:.4f}")
            
            # Show the last 10 records
            print("\nLast 10 records:")
            print(display_df.tail(10).to_string(index=False))
        
        return display_df
        
    except Exception as e:
        print(f"Error querying InfluxDB: {e}")
        return None

if __name__ == "__main__":
    hours = 24
    print(f"Querying USD/TRY exchange rates for the past {hours} hours...")
    query_exchange_rates(hours) 