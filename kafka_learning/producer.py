from confluent_kafka import Producer 
from confluent_kafka.admin import AdminClient, NewTopic
import json, time 

admin = AdminClient({'bootstrap.servers': 'localhost:9092'})
topic_name = 'user_events'
new_topic = NewTopic(topic_name, num_partitions=3, replication_factor=1)
result = admin.create_topics([new_topic])
for topic, res in result.items():
    try:
        res.result()
        print(f'Topic {topic} created successfully.')
    except Exception as e:
        print(f'Failed to create topic {topic}: {e}')

producer = Producer({'bootstrap.servers':'localhost:9092' })

def delivery_report(err,msg):
    if err:
        print(f'Delivery failed : {err}')
    else:
        print(f'Delivery successful : {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

for i in range(10):
    event = {
        'user_id': f'user_{i}',
        'action': 'page_view',
        'timestamp': int(time.time()),
        'page': f'/product/{i *3}'
    }
    producer.produce(
        topic = 'user_events',
        value = json.dumps(event),
        key = event['user_id'],
        callback = delivery_report
    )
    
    producer.poll(0)
producer.flush()
print('Done!')