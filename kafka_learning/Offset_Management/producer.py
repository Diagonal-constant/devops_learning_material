from confluent_kafka import Producer 
from confluent_kafka.admin import AdminClient, NewTopic
import json, time 

admin = AdminClient({'bootstrap.servers': 'localhost:9092'})
topic_name = 'orders_'
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

i = 0
while True:
    i += 1
    event = {
        'order_id': f'order_{i}',
        'customer': f'Customer_{i}',
        'amount': round(100 + i * 10, 2)
    }
    producer.produce(
        topic = 'orders_',
        value = json.dumps(event),
        key = str(i),
        callback = delivery_report
    )
    
    producer.poll(1)
    
producer.flush()
print('Done!')