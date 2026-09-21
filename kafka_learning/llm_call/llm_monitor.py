from confluent_kafka import Consumer 
import json 
from collections import defaultdict 

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'llm_monitor_group',
    'auto.offset.reset': 'earliest' 
})

consumer.subscribe(['llm_logs'])

stats = defaultdict(lambda: {
    'calls':0,
    'tokens':0,
    'latency':0.0 
})

COST_TOKEN = 0.0000015

while True:
    msg = consumer.poll(1.0)
    
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue
    
    data = json.loads(msg.value().decode('utf-8'))
    
    uid = data['user_id']
    s = stats[uid] 
    s['calls'] += 1
    s['tokens'] += data['tokens_in_use']
    s['latency'] += data['latency_seconds']
    
    cost = s['tokens'] * COST_TOKEN
    avg_lat = s['latency'] / s['calls']
    
    print(f"User: {uid} | Calls: {s['calls']} | Tokens: {s['tokens']} | Cost: ${cost:.4f} | Avg Latency: {avg_lat:.2f}s")