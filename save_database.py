import requests
from datetime import datetime
import time
import random
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import xml.etree.ElementTree as ET

# InfluxDB connection parameters
INFLUXDB_URL = "http://localhost:8087"
# Get a new token from InfluxDB UI with read/write permissions
INFLUXDB_TOKEN = "CUuxTbAY5jhbhL3RV8HUPJNAXC9P_1ZjQ5hzMK05nKR3iFl8vWF8ESLrkS7IYu7_nEU1yOY6Qvx6xqQ2wU1R7A=="  # Replace with your new token
INFLUXDB_ORG = "MyWork"  # This should match your organization name in InfluxDB
INFLUXDB_BUCKET = "exchange_rates"

# TCMB Exchange Rate API endpoint (no API key required)
TCMB_API_URL = "https://www.tcmb.gov.tr/kurlar/today.xml"

def initialize_influxdb():
    try:
        # Create a client to connect to InfluxDB with token authentication
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        
        # Check if the bucket exists, if not create it
        buckets_api = client.buckets_api()
        buckets = buckets_api.find_buckets().buckets
        bucket_names = [bucket.name for bucket in buckets]
        
        if INFLUXDB_BUCKET not in bucket_names:
            print(f"Bucket '{INFLUXDB_BUCKET}' does not exist. Creating it...")
            buckets_api.create_bucket(bucket_name=INFLUXDB_BUCKET, org=INFLUXDB_ORG)
            print(f"Bucket '{INFLUXDB_BUCKET}' created successfully!")
        else:
            print(f"Bucket '{INFLUXDB_BUCKET}' already exists.")
            
        print("InfluxDB connection initialized successfully.")
        client.close()
    except Exception as e:
        print(f"Error initializing InfluxDB: {e}")

def fetch_exchange_rate():
    try:
        # Make request with a timeout to ensure we don't hang
        response = requests.get(TCMB_API_URL, timeout=10)
        # Print the response for debugging
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"API error: {response.status_code} - {response.text}")
            return None
        
        # Parse XML data
        root = ET.fromstring(response.content)
        
        # Find USD/TRY exchange rate
        usd_try_rate = None
        for currency in root.findall('./Currency'):
            if currency.get('Kod') == 'USD':
                # Get the ForexBuying value (or BanknoteBuying if preferred)
                usd_try_rate = float(currency.find('ForexBuying').text.replace(',', '.'))
                break
        
        if usd_try_rate:
            # For demonstration purposes only: add some random fluctuation
            # to make the visualization more interesting
            # Remove this in production
            small_fluctuation = random.uniform(-0.05, 0.05)
            usd_try_rate = usd_try_rate + small_fluctuation
            return usd_try_rate
        else:
            print("USD/TRY rate not found in TCMB data")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def save_to_database(rate):
    if rate is None:
        return
    
    try:
        # Create a client to connect to InfluxDB with token authentication
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        # Create a data point
        point = Point("usd_to_try") \
            .tag("source", "tcmb") \
            .field("rate", rate) \
            .time(datetime.utcnow())
        
        # Write the data to InfluxDB
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        client.close()
    except Exception as e:
        print(f"Error saving to InfluxDB: {e}")

def main():
    print("Initializing InfluxDB...")
    initialize_influxdb()
    
    print("Starting to fetch and save exchange rates...")
    while True:
        try:
            rate = fetch_exchange_rate()
            if rate:
                save_to_database(rate)
                print(f"Saved rate: {rate:.3f} at {datetime.now()}")
            time.sleep(20)  # Wait 20 seconds between fetches
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(20)  # Wait 20 seconds before retrying

if __name__ == "__main__":
    main()