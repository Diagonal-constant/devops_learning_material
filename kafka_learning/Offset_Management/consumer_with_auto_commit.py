import json
import sqlite3
from confluent_kafka import Consumer
from process_msg import process, init_db

DB_NAME = 'orders.db'

# 1. Initialize schema setup
init_db(DB_NAME)

# 2. Setup Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id':          'auto-group',
    'enable.auto.commit': 'true',         
    'auto.commit.interval.ms': '5000',   
    'auto.offset.reset': 'earliest',
})
consumer.subscribe(['orders_'])

# 3. Open ONE persistent connection for the lifecycle of the loop
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print("Kafka consumer started with a persistent DB connection. Listening...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None: 
            continue
        if msg.error(): 
            print(f"Consumer error: {msg.error()}")
            continue

        try:
            # Decode message payload
            data = json.loads(msg.value().decode('utf-8'))

            # Pass the open cursor and connection directly! Zero overhead.
            process(cursor, conn, data)  

            print(f"[AUTO] Saved {data['order_id']} | partition={msg.partition()} offset={msg.offset()}")
        
        except json.JSONDecodeError:
            print("Received malformed JSON message from Kafka; skipping processing.")
        except KeyError as e:
            print(f"Missing required key in message payload: {e}")
        except Exception as e:
            print(f"Unexpected error processing message: {e}")

except KeyboardInterrupt:
    print("\nStopping consumer gracefully...")

finally:
    # 4. Clean up resources completely when the loop terminates
    print("Closing database connections and Kafka consumer...")
    cursor.close()
    conn.close()
    consumer.close()