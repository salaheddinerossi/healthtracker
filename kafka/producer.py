from confluent_kafka import Producer
from pymongo import MongoClient
from faker import Faker
from datetime import datetime
import json
import random
import time

# Define the Kafka configuration
conf = {'bootstrap.servers': 'localhost:9092'}

# Create a Producer instance with the configuration
producer = Producer(conf)

# Initialize Faker
fake = Faker()

# Create a MongoDB client
client = MongoClient('mongodb+srv://sdrossi:imane123@cluster0.53siks7.mongodb.net/')

# Access the 'clients' collection in the 'health' database
db = client['HealthTracking']
clients_collection = db['Client']

# Fetch user IDs from the 'clients' collection (assuming the field for user ID is 'userId')
user_ids = [str(client['_id']) for client in clients_collection.find()]

while True:
    for user_id in user_ids:
        # Generate fake vital signs
        blood_pressure = fake.random_int(min=80, max=120)
        body_temperature = round(random.uniform(36.5, 37.5), 1)
        heart_beat = fake.random_int(min=60, max=100)

        # Construct message
        message = {
            'userId': user_id,
            'bloodPressure': blood_pressure,
            'bodyTemperature': body_temperature,
            'heartBeat': heart_beat,
            'timestamp': int(time.time())  # UNIX timestamp
        }

        # Produce a message to the 'vitalSigns' topic
        producer.produce('vitalSigns', value=json.dumps(message))

        # Wait for any outstanding messages to be delivered and delivery reports to be acknowledged.
        producer.flush()
        
        print(message)

        # Sleep for a while
    time.sleep(15)
