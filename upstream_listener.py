import pika
import time
import os
import multiprocessing as mp
con_down=None

def connect_down_stream():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('sender_queue'),durable=True)
    return channel


def start_simple_socket():
    from simple_socket import SimpleWebSocketServer,SimpleEcho
    server = SimpleWebSocketServer('0.0.0.0', 8000, SimpleEcho)
    server.serveforever()

if __name__=='__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0'))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('receiver_queue'),durable=True)
    res=mp.Process(target=start_simple_socket)
    res.start()


    def sleep():
        time.sleep(60)

    def callback(ch, method, properties, body):
        print('messag received')
        f = open("status.txt", "w")
        f.write(os.environ.get('src_system'))
        f.close()
        sleep()
        global con_down
        if con_down == None:
            con_down=connect_down_stream()
        con_down.basic_publish(body='SETTLE', exchange='', routing_key=os.environ.get('sender_queue'))

    channel.basic_consume(queue =os.environ.get('receiver_queue'),auto_ack = True,on_message_callback = callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()