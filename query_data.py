from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np

# InfluxDB connection parameters - match save_database.py
INFLUXDB_URL = "http://localhost:8087"
INFLUXDB_TOKEN = "CUuxTbAY5jhbhL3RV8HUPJNAXC9P_1ZjQ5hzMK05nKR3iFl8vWF8ESLrkS7IYu7_nEU1yOY6Qvx6xqQ2wU1R7A=="
INFLUXDB_ORG = "MyWork"
INFLUXDB_BUCKET = "exchange_rates"

def query_exchange_rates(hours=24, visualize=True):
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
        
        # Sort by time to ensure chronological order
        display_df = display_df.sort_values('Time')
        
        # Calculate statistics
        if not display_df.empty:
            min_rate = display_df['USD/TRY Rate'].min()
            max_rate = display_df['USD/TRY Rate'].max()
            avg_rate = display_df['USD/TRY Rate'].mean()
            std_dev = display_df['USD/TRY Rate'].std()
            volatility = (max_rate - min_rate) / avg_rate * 100  # Volatility as percentage
            
            print(f"\nStatistics for the past {hours} hours:")
            print(f"Minimum Rate: {min_rate:.4f}")
            print(f"Maximum Rate: {max_rate:.4f}")
            print(f"Average Rate: {avg_rate:.4f}")
            print(f"Standard Deviation: {std_dev:.4f}")
            print(f"Volatility: {volatility:.2f}%")
            
            # Show the last 10 records
            print("\nLast 10 records:")
            print(display_df.tail(10).to_string(index=False))
            
            if visualize and len(display_df) > 1:
                try:
                    visualize_data(display_df, hours)
                except Exception as e:
                    print(f"Error visualizing data: {e}")
        
        return display_df
        
    except Exception as e:
        print(f"Error querying InfluxDB: {e}")
        return None

def visualize_data(data_df, hours):
    """Generate a visualization of the exchange rate data"""
    plt.figure(figsize=(12, 6))
    
    # Plot the exchange rate over time
    plt.plot(data_df['Time'], data_df['USD/TRY Rate'], 'b-', label='USD/TRY Rate')
    
    # Add a trend line
    z = np.polyfit(range(len(data_df)), data_df['USD/TRY Rate'], 1)
    p = np.poly1d(z)
    plt.plot(data_df['Time'], p(range(len(data_df))), "r--", label='Trend')
    
    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Exchange Rate (USD/TRY)')
    plt.title(f'USD to TRY Exchange Rate - Past {hours} Hours')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format the date on x-axis
    plt.gcf().autofmt_xdate()
    date_format = DateFormatter("%m-%d %H:%M")
    plt.gca().xaxis.set_major_formatter(date_format)
    
    # Add statistics to the plot
    min_rate = data_df['USD/TRY Rate'].min()
    max_rate = data_df['USD/TRY Rate'].max()
    avg_rate = data_df['USD/TRY Rate'].mean()
    plt.axhline(y=avg_rate, color='g', linestyle='-', alpha=0.3, label=f'Avg: {avg_rate:.4f}')
    
    # Annotate min and max points
    min_idx = data_df['USD/TRY Rate'].idxmin()
    max_idx = data_df['USD/TRY Rate'].idxmax()
    plt.plot(data_df.loc[min_idx, 'Time'], min_rate, 'go', markersize=8)
    plt.plot(data_df.loc[max_idx, 'Time'], max_rate, 'ro', markersize=8)
    
    # Save the plot
    plt.tight_layout()
    filename = f"usd_try_exchange_rate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    print(f"\nVisualization saved as {filename}")
    
    # Show the plot
    plt.show()

def main():
    hours = int(input("Enter the number of hours to query (default 24): ") or 24)
    visualize = input("Generate visualization? (y/n, default y): ").lower() != 'n'
    
    print(f"\nQuerying USD/TRY exchange rates for the past {hours} hours...")
    query_exchange_rates(hours, visualize)

if __name__ == "__main__":
    main() 