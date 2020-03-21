import pika
import time
import os
con_down=None
import requests

def connect_down_stream():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('sender_queue'),durable=True)
    return channel


if __name__=='__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('receiver_queue'),durable=True)


    def sleep():
        time.sleep(120)

    def callback(ch, method, properties, body):
        print('messag received')
        dictToSend = {'status': os.environ.get('src_system')}
        requests.post('http://'+str(os.environ.get('tracer_ip'))+':'+5000+'/soc', json=dictToSend)
        sleep()
        global con_down
        if con_down == None:
            con_down=connect_down_stream()
        con_down.basic_publish(body='SETTLE', exchange='', routing_key=os.environ.get('sender_queue'))

    channel.basic_consume(queue =os.environ.get('receiver_queue'),auto_ack = True,on_message_callback = callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()