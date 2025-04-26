import yfinance as yf
import psycopg2
from datetime import datetime
import time

DB_PARAMS = {
    'dbname': 'doviz',
    'user': 'postgres',
    'password': '03806',
    'host': 'localhost',
    'port': '5432'
}

def create_table():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = 'exchange_rates'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            print("Table 'exchange_rates' does not exist. Creating it...")
            cur.execute("""
                CREATE TABLE exchange_rates (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP,
                    usd_to_try_rate DECIMAL(10, 4)
                )
            """)
            conn.commit()
            print("Table 'exchange_rates' created successfully!")
        else:
            print("Table 'exchange_rates' already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in create_table: {e}")

def fetch_exchange_rate():
    try:
        ticker = yf.Ticker("USDTRY=X")
        current_price = ticker.info['regularMarketPrice']
        return float(current_price)
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def save_to_database(rate):
    if rate is None:
        return
        
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO exchange_rates (timestamp, usd_to_try_rate) VALUES (%s, %s)",
        (datetime.now(), rate)
    )
    
    conn.commit()
    cur.close()
    conn.close()

def main():
    print("Creating table if it doesn't exist...")
    create_table()
    
    print("Starting to fetch and save exchange rates...")
    while True:
        try:
            rate = fetch_exchange_rate()
            if rate:
                save_to_database(rate)
                print(f"Saved rate: {rate:.3f} at {datetime.now()}")
            time.sleep(30)  
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(30)  

if __name__ == "__main__":
    main()