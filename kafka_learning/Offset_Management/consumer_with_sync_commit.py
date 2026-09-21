from confluent_kafka import Consumer
import json, sqlite3

from process_msg import init_db,process

DB_NAME = 'orders.db'

# 1. Initialize schema setup
init_db(DB_NAME)


consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id':          'sync-group',
    'enable.auto.commit': 'false',   # WE commit manually
    'auto.offset.reset':  'earliest',
})

consumer.subscribe(['orders_'])
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None: continue
    if msg.error(): continue

    data = json.loads(msg.value().decode())

    # Pass the open cursor and connection directly! Zero overhead.
    process(cursor, conn, data)  
       
    print(f"[SYNC] Saved {data['order_id']} Partition {msg.partition()}, offset={msg.offset()}")

    # STEP 2: commit AFTER work is done — blocks until broker confirms
    consumer.commit(asynchronous=False)
    print(f"[SYNC] Committed offset={msg.offset()}")