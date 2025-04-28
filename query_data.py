from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import pandas as pd

# InfluxDB connection parameters - must match save_database.py
INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_USER = "emiraka"  # Your username
INFLUXDB_PASS = "emir16gs"  # Your password
INFLUXDB_DB = "exchange_rates"  # The database to query

def query_exchange_rates(hours=24):
    """Query exchange rates for the last specified hours"""
    try:
        # Create a client connection to InfluxDB with authentication
        client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, 
                               username=INFLUXDB_USER, password=INFLUXDB_PASS,
                               database=INFLUXDB_DB)
        
        # Prepare time range for query
        time_now = datetime.utcnow()
        time_from = time_now - timedelta(hours=hours)
        time_from_str = time_from.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # InfluxQL query (used in InfluxDB 1.x)
        query = f"SELECT * FROM usd_to_try WHERE time > '{time_from_str}'"
        
        # Execute the query
        result = client.query(query)
        client.close()
        
        # Convert to pandas DataFrame
        if not result:
            print("No data found")
            return None
            
        points = list(result.get_points(measurement='usd_to_try'))
        if not points:
            print("No data found")
            return None
            
        result_df = pd.DataFrame(points)
        
        # Process the result for display
        print(f"Retrieved {len(result_df)} records from the past {hours} hours")
        
        # Display the results
        display_df = result_df[['time', 'rate']].rename(columns={
            'time': 'Time', 
            'rate': 'USD/TRY Rate'
        })
        
        # Convert the time string to datetime
        display_df['Time'] = pd.to_datetime(display_df['Time'])
        
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