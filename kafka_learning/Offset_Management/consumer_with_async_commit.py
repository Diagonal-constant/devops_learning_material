from confluent_kafka import Consumer
import json, sqlite3
from process_msg import init_db,process

DB_NAME = 'orders.db'
# 1. Initialize schema setup
init_db(DB_NAME)


# this fires LATER when Kafka responds to our commit
def on_commit(err, partitions):
    if err:
        print(f"COMMIT FAILED: {err}")
    else:
        for p in partitions:
            print(f"[ASYNC] Broker confirmed P{p.partition} @ offset {p.offset}")

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id':          'async-group',
    'enable.auto.commit': 'false',
    'auto.offset.reset':  'earliest',
    'on_commit': on_commit   # register callback
})
consumer.subscribe(['orders_'])

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None: continue
    if msg.error(): continue

    data = json.loads(msg.value().decode())

    process(cursor, conn, data)
    print(f"[ASYNC] Saved {data['order_id']} Partition {msg.partition()}, offset={msg.offset()}")

    # STEP 2: send commit — returns IMMEDIATELY, does not block
    consumer.commit(asynchronous=True)
    print(f"[ASYNC] Moving to next message (commit in flight)")
