import pika,json
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

def product1data(id_):
    try:
        from testrab.models import Product
        from testrab.serializer import ProductSerializer
        obj = Product.objects.filter(id=id_)#.values('id')
        serializer = ProductSerializer(obj, many=True)
        return serializer.data
    except Exception as e:
        return f"{id_} not working vro {e} "

 

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    # response = fib(n)
    response = product1data(n)
    print(response)
    # try:
    #     response = product1data(n)
    #     print(str(rfilteresponse))
    # except Exception as e:
    #     print(e)
    #     response = fib(n)filter
    #     print(response)
    # try:
    #     print(response)
    # except Exception as e:
    #     print(e)
    # json.dumps(body)
    ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                        props.correlation_id),
                    # body=str({response}))
                    body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
# channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

# print(" [x] Awaiting RPC requests")
# channel.start_consuming()

def main():
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()


# from background_task import background
# # from django.contrib.auth.models import User
# @background(schedule=60)
# def notify_user():
#     # lookup user by id and send them a message
#     print("django is running ....!")
    # user = User.objects.get(pk=user_id)
    # user.email_user('Here is a notification', 'You have been notified')