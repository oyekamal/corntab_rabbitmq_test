#amqps://jdbfsffv:q0qNYM29La7lp8D-agpQQRa5GLaKyCBp@jellyfish.rmq.cloudamqp.com/jdbfsffv

import pika , json

params = pika.URLParameters('amqps://jdbfsffv:q0qNYM29La7lp8D-agpQQRa5GLaKyCBp@jellyfish.rmq.cloudamqp.com/jdbfsffv')
# params = pika.ConnectionParameters('amqps://jdbfsffv:q0qNYM29La7lp8D-agpQQRa5GLaKyCBp@jellyfish.rmq.cloudamqp.com/jdbfsffv')


connection = pika.BlockingConnection(params)

channel = connection.channel()

    
    
# def publish1():
#     channel.basic_publish(exchange='', routing_key='main', body='hello world')
#     # channel.basic_publish(exchange='', routing_key='admin', body='hello world bro')
    
def publish(method, body):
    import pika , json

    params = pika.URLParameters('amqps://jdbfsffv:q0qNYM29La7lp8D-agpQQRa5GLaKyCBp@jellyfish.rmq.cloudamqp.com/jdbfsffv')
    # params = pika.ConnectionParameters('amqps://jdbfsffv:q0qNYM29La7lp8D-agpQQRa5GLaKyCBp@jellyfish.rmq.cloudamqp.com/jdbfsffv')


    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    print('publish running')
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
    
# connection.close()