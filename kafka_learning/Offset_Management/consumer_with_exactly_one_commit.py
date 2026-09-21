"""
Imagine a bank: you read "transfer £100 from A to B", you debit A, you credit B, 
you mark the instruction as done. If the system crashes after debiting A but before 
crediting B — you've lost £100. A transaction makes the three steps atomic: either 
all happen together or none do.
Kafka transactions work the same way — the three steps are: consume the input message,
produce the output message, commit the input offset.
"""

from confluent_kafka import Consumer, Producer
import json

# --- CONSUMER: reads from input topic ---
consumer = Consumer({
    'bootstrap.servers':  'localhost:9092',
    'group.id':           'eos-group',
    'enable.auto.commit':  'false',       # offset committed INSIDE transaction
    'isolation.level':     'read_committed',# only see committed transaction output
    'auto.offset.reset':  'earliest',
})

consumer.subscribe(['orders'])

# --- PRODUCER: writes to output topic ---
producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'transactional.id':  'order-processor-1',  # unique ID per producer instance
    'enable.idempotence': 'true',
})

# register this producer with Kafka brokers
producer.init_transactions()


while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None: continue
    if msg.error(): continue

    data = json.loads(msg.value().decode())
    print(f"Read: {data['order_id']} offset={msg.offset()}")

    try:
        # ── TRANSACTION BEGINS ──────────────────────────────
        producer.begin_transaction()

        # YOUR WORK: enrich the order
        enriched = {
            **data,
            'tax':    round(data['amount'] * 0.15, 2),
            'total':  round(data['amount'] * 1.15, 2),
            'status': 'confirmed'
        }

        # INSIDE TRANSACTION: produce to output topic
        # (message is written but NOT visible to consumers yet)
        producer.produce(
            'orders-confirmed',
            key=data['order_id'].encode(),
            value=json.dumps(enriched).encode()
        )
        print(f"Produced enriched order (pending, not visible yet)")

        # INSIDE TRANSACTION: include the consumer offset
        # this makes the offset commit part of the same atomic operation
        producer.send_offsets_to_transaction(
            {msg.topic(): {msg.partition(): msg.offset() + 1}},
            consumer.consumer_group_metadata()
        )

        # COMMIT: output becomes visible + offset moves — simultaneously
        producer.commit_transaction()
        print(f"Transaction committed — output visible, offset moved")
        # ── TRANSACTION ENDS ────────────────────────────────

    except Exception as e:
        print(f"Error: {e} — aborting transaction")
        producer.abort_transaction()
        # output message disappears, offset stays where it was, retry next loop