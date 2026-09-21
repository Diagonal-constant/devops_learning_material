from confluent_kafka import Consumer
import json 

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_consumer_group',
    'auto.offset.reset': 'earliest' 
})

consumer.subscribe(['user_events'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f'Error: {msg.error()}')
            continue
        
        event = json.loads(msg.value().decode('utf-8'))
        # print(f'[Partition {msg.partition()}, Offset {msg.offset()}]')
        print(f"  User: {event['user_id']} visited {event['page']}")
        # print(f'Received event: {event}')
        
        
        
except KeyboardInterrupt:
    pass
finally:
    consumer.close()  # always close to commit final offsets and clean up resources