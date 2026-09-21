from confluent_kafka import Producer
import json, time, random
from confluent_kafka.admin import AdminClient, NewTopic

# ── Step 1: Create topics ─────────────────────────────────────────────────────
admin = AdminClient({'bootstrap.servers': 'localhost:9092'})

topics = [
    NewTopic('raw-events',  num_partitions=3, replication_factor=1),
    NewTopic('ml-features', num_partitions=3, replication_factor=1),
]

results = admin.create_topics(topics)
for topic, future in results.items():
    try:
        future.result()
        print(f'Created topic: {topic}')
    except Exception as e:
        print(f'Topic ready: {topic} ({e})')

# ── Step 2: Producer setup ────────────────────────────────────────────────────
producer = Producer({'bootstrap.servers': 'localhost:9092'})

PAGES = ['/home', '/product/shoes', '/product/bag', '/checkout', '/cart']
USERS = [f'user_{i}' for i in range(50)]

def delivery_report(err, msg):
    if err:
        print(f'[ERROR] Delivery failed: {err}')
    else:
        print(f'[SENT]  {msg.key().decode()} → partition {msg.partition()} @ offset {msg.offset()}')

def make_event():
    return {
        'user_id': random.choice(USERS),
        'page': random.choice(PAGES),
        'timestamp': int(time.time()),
        'device': random.choice(['mobile', 'desktop', 'tablet']),
        'session_id': f'session_{random.randint(1000, 9999)}'
    }

# ── Step 3: Produce forever ───────────────────────────────────────────────────
print('Sending user events to Kafka...')

try:
    while True:
        event = make_event()
        producer.produce(
            'raw-events',
            key=event['user_id'],
            value=json.dumps(event),
            callback=delivery_report      # added
        )
        producer.poll(0)
        time.sleep(0.2)

except KeyboardInterrupt:
    print('\nStopping producer...')

finally:
    producer.flush()                      # wait for all queued messages to deliver
    print('All messages flushed. Done.')