from flask import Flask, jsonify
from flask import Blueprint
from flask import request
import os,json,sys
import time,math,random
from pykafka import KafkaClient
"""Produce fake transactions into a Kafka topic."""
from time import sleep
from kafka import KafkaProducer
from transactions import create_random_transaction
generator_api = Blueprint('generator_api', __name__)
TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND

def get_kafka_client():
    kafkabrokerup=True
    while kafkabrokerup:
        try:
            kafka_client=KafkaClient(hosts=KAFKA_BROKER_URL)
            kafkabrokerup=False
        except:
            kafkabrokerup=True
    return kafka_client

@generator_api.route('/producer', methods=['POST'])
def producer():
    print(TRANSACTIONS_TOPIC)
    print(KAFKA_BROKER_URL)
    print(TRANSACTIONS_PER_SECOND)
    try:
        client = get_kafka_client()
        topic = client.topics[TRANSACTIONS_TOPIC]
        producer = topic.get_sync_producer()
        count=6
        transactions=[]
        while count>0:
            try:
                transaction: dict = create_random_transaction()
                transaction_output=json.dumps(transaction)
                producer.produce(transaction_output.encode('ascii'))
                print(transaction)  # DEBUG
                sleep(SLEEP_TIME)
                transactions.append(transaction)
                count=count-1
                print(transactions)
            except Exception as e:
                print(str(e))
        return({"statusCode": 200,"body": transactions,"KAFKA_BROKER_URL": KAFKA_BROKER_URL})
    except Exception as e:
        return({"statusCode": 400,"error_message": str(e)})