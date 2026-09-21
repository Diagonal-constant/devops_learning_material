from confluent_kafka import Consumer
import json, numpy as np

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'model-inference',
    'auto.offset.reset': 'latest'
})
consumer.subscribe(['ml-features'])

# Simulated trained model weights
# In production: model = mlflow.sklearn.load_model('models:/recommender/3')
WEIGHTS = np.array([0.3, 0.5, 0.1, 0.4, -0.2])
BIAS = -2.0

def predict_purchase_prob(f):
    x = np.array([f['page_views'], f['unique_pages'],
                  f['session_duration_sec'], f['is_mobile'], f['on_checkout']])
    logit = x @ WEIGHTS + BIAS
    return float(1 / (1 + np.exp(-logit)))

while True:
    msg = consumer.poll(1.0)
    if msg is None or msg.error(): continue

    features = json.loads(msg.value())
    prob = predict_purchase_prob(features)

    if prob > 0.7:
        print(f"[OFFER]  Show {features['user_id']} a 10% discount!  ({prob:.0%})")
    else:
        print(f"[PASS]   {features['user_id']} probability: {prob:.0%}")