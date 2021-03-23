import time 
# from testrab.models import Product1
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

        connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host='localhost'))
        # connection = pika.BlockingConnection(params)
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
        
        
def server():
    import pika

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')


    def fib(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            print(n)
            # return fib(n - 1) + fib(n - 2)
            return n*n
    
    # def product1data(id_):
    #     from testrab.models import Product1
    #     from testrab.serializer import Product1Serializer
    #     obj = Product1.objects.filter(id=id_)
    #     serializer = Product1Serializer(obj)
    #     return serializer.data


    def on_request(ch, method, props, body):
        n = int(body)

        print(" [.] fib(%s)" % n)
        response = fib(n)
        # response = product1data(n)
        # try:
        #     print(response)
        # except Exception as e:
        #     print(e)
        # json.dumps(body)
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
    