from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json

# Define the Kafka configuration
conf = {'bootstrap.servers': 'localhost:9092', 'group.id': 'group1', 'auto.offset.reset': 'earliest'}

# Create a Consumer instance with the configuration
consumer = Consumer(conf)

# Subscribe to the 'vitalSigns' topic
consumer.subscribe(['vitalSigns'])

# Create a MongoDB client
client = MongoClient('mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/')

# Access the 'vitalSigns' collection in the 'health' database
db = client['HealthTracking']
collection = db['vitalSigns']

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    # Parse message
    print(msg)
    message = json.loads(msg.value().decode('utf-8'))

    # Insert the message into the MongoDB collection
    collection.insert_one(message)

consumer.close()

