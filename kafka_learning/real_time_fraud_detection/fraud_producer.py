from confluent_kafka import Producer 
import json, time, random 
from confluent_kafka.admin import AdminClient, NewTopic 

# ── Step 1: Create topics ─────────────────────────────────────────────────────
admin = AdminClient({'bootstrap.servers': 'localhost:9092'})
topic = NewTopic('transactions', num_partitions=3, replication_factor=1)
 result = admin.create_topics([topic])
for topic, future in result.items():
    try:
        future.result()
        print(f'Created topic: {topic}')
    except Exception as e:
        print(f'Topic ready: {topic} ({e})')
        
        
# ── Step 2: Producer setup ────────────────────────────────────────────────────
producer = Producer({'bootstrap.servers': 'localhost:9092'}) 

def make_transaction():
    is_fraud = random.random() < 0.10 
    return {
        'transaction_id': f'tx_{random.randint(10000, 99999)}',
        'user_id': f'user_{random.randint(1, 50)}',
        'amount': round(random.uniform(500, 1000), 2) if is_fraud else round(random.uniform(10, 100), 2),
        'merchant': random.choice(['electronics', 'clothing', 'grocery', 'travel']),
        'country': random.choice(['US', 'UK', 'CA', 'AU']) if is_fraud else 'BD',
        'timestamp': int(time.time())
    }
    
try:
    while True:
        transaction = make_transaction()
        producer.produce(
            'transactions',
            key=transaction['transaction_id'],
            value=json.dumps(transaction)
        )
        producer.poll(0)
        time.sleep(0.5)
except KeyboardInterrupt:
    print('\nStopping producer...')
finally:
    producer.flush()