import time 
from testrab.models import Product1
import pika, json
def my_cron_job():
    print("hello im running.... ")
    print("Do something about me")
    prod = Product1.objects.values_list()
    print(prod)
    # print(time.time())
    # your functionality goes here
    
    
def consumer_cronjob():
        import pika, json

        params = pika.URLParameters('amqps://jdbfsffv:q0qNYM29La7lp8D-agpQQRa5GLaKyCBp@jellyfish.rmq.cloudamqp.com/jdbfsffv')
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='main')
        def callback(ch,method,properties, body):
            print("received in main")
            # print(body)
            print("properties -- ",properties.content_type)
            data = json.loads(body)
            if properties.content_type == 'product_created':
                try:
                    from testrab.models import Product1

                    print("inside working ...?")
                    p=Product1.objects.create(title=data['title'], image=data['image'])
                    p.save()
                    
                    # all_=Product.objects.values()
                    # print('yes created ----->',all_)
                    print(data)
                    print("all data store in product1 =---< ",Product1.objects.values())
                except Exception as e:
                    print("exception --- > ",e)
            elif properties.content_type == 'product_deleted':
                print('deleted -----<')
                
        channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
        print("started consumming")
        channel.start_consuming()
        channel.close()