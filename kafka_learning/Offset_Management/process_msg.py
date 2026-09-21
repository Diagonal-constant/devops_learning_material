import json
import sqlite3

def init_db(db_name):
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY, 
            customer TEXT, 
            amount REAL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def process(cursor, conn, msg):
    """
    Processes and inserts data using a PERSISTENT cursor and connection.
    Does NOT open or close connections on its own.
    """
    try:
        if isinstance(msg, str):
            data = json.loads(msg)
        else:
            data = msg
    except Exception as e:
        print(f"Failed to parse message: {e}")
        return

    try:
        cursor.execute('''
            INSERT INTO orders (order_id, customer, amount) 
            VALUES (?, ?, ?)
        ''', (data['order_id'], data['customer'], data['amount']))
        
        # Commit the transaction to ensure data is written safely
        conn.commit()
        print(f"Order {data['order_id']} processed successfully.")
        
    except sqlite3.IntegrityError:
        print(f"Error: Order ID {data['order_id']} already exists.")
    except Exception as e:
        print(f"An error occurred during database insertion: {e}")