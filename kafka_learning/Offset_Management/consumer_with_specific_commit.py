"""Specific offset commit — commit exact offset after batch processing
Instead of committing "wherever I am right now", you tell Kafka exactly which offset to commit. Useful when you collect 100 messages,
bulk-insert them to a database in one query, then commit the last offset of that batch — saving 99 round-trips."""


from confluent_kafka import Consumer, TopicPartition
import json, sqlite3
from process_msg import init_db,process

DB_NAME = 'orders.db'

# 1. Initialize schema setup
init_db(DB_NAME)

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id':          'batch-group',
    'enable.auto.commit': 'false',
    'auto.offset.reset':  'earliest',
})
consumer.subscribe(['orders_'])

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

batch = []

while True:
    msg = consumer.poll(timeout=1.0)
    if msg and not msg.error():
        batch.append(msg)
        print(f"Collected offset={msg.offset()} (batch size={len(batch)})")

    if len(batch) >= 5:   # using 5 here so output is short — use 100 in prod

        # bulk insert all 5 messages in ONE database call
        rows = [json.loads(m.value().decode()) for m in batch]
        cursor.executemany('INSERT OR IGNORE INTO orders VALUES (?,?,?)',
                           [(r['order_id'], r['customer'], r['amount']) for r in rows])
        conn.commit()
        print(f"Bulk inserted {len(batch)} rows")

        # commit highest offset per partition — offset+1 = "start here next time"
        offsets = {}
        for m in batch:
            k = (m.topic(), m.partition())
            if k not in offsets or m.offset() > offsets[k].offset - 1:
                offsets[k] = TopicPartition(m.topic(), m.partition(), m.offset() + 1)

        consumer.commit(offsets=list(offsets.values()), asynchronous=False)
        print(f"Committed: {[(k, v.offset) for k, v in offsets.items()]}")
        batch = []   # reset batch