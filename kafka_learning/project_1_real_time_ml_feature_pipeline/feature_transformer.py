from confluent_kafka import Consumer, Producer 
import json, time 
from collections import defaultdict 

consumer  =Consumer({
    'bootstrap.servers':'localhost:9092',
    'group.id':'feature_transformer_group',
    'auto.offset.reset':'latest'
})

producer = Producer({'bootstrap.servers':'localhost:9092'})

user_state = defaultdict(lambda: {
    'page_views': 0,
    'pages_seen': set(),
    'last_device': None,
    'session_start' : None
})

consumer.subscribe(['raw-events'])
print('Transforming events and producing features...')

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        continue
    
    event = json.loads(msg.value().decode('utf-8'))
    user_id = event['user_id']
    
    state = user_state[user_id]
    state['page_views'] += 1
    state['pages_seen'].add(event['page'])
    state['last_device'] = event['device']
    
    if state['session_start'] is None:
        state['session_start'] = event['timestamp']
    
    features = {
    'user_id': user_id,
    'page_views': state['page_views'],
    'unique_pages': len(state['pages_seen']),
    'session_duration_sec': event['timestamp'] - state['session_start'],  # renamed
    'is_mobile': 1 if state['last_device'] == 'mobile' else 0,            # added
    'on_checkout': 1 if event['page'] == '/checkout' else 0               # added
    }
    
    producer.produce(
        'ml-features',
        key = user_id,
        value = json.dumps(features)
    )
    producer.poll(0)