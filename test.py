import multiprocessing as mp
import pika
import time
import os
con_down=None
con_gcd=None
import requests

def connect_mq(mq):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.99.100'))
    channel = connection.channel()
    channel.queue_declare(queue=mq, durable=True)
    return channel

def upstream_listner():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.99.100'))
    channel = connection.channel()
    channel.queue_declare(queue='upstream', durable=True)

    def callback(ch, method, properties, body):
        print('messag received')
        dictToSend = {'status': 'UP'}
        requests.post('http://'+'127.0.0.1'+':'+str(5000)+'/soc', json=dictToSend)
        time.sleep(120)
        con_down=connect_mq('downstream1')
        con_down.basic_publish(body='UP', exchange='', routing_key='downstream1')
        con_down.close()

    channel.basic_consume(queue = 'upstream',auto_ack = True,on_message_callback = callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def downstream_listner():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.99.100'))
    channel = connection.channel()
    channel.queue_declare(queue='downstream1', durable=True)

    def callback(ch, method, properties, body):
        print('messag received')
        dictToSend = {'status': 'DOWN'}
        requests.post('http://' + '127.0.0.1' + ':' + str(5000) + '/soc', json=dictToSend)
        time.sleep(120)
        con_down = connect_mq('downstream2')
        con_down.basic_publish(body='DOWN', exchange='',routing_key='downstream2')
        con_down.close()

    channel.basic_consume(queue='downstream1', auto_ack=True, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def gcd_listner():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.99.100'))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('receiver_queue'), durable=True)

    def callback(ch, method, properties, body):
        print('messag received')
        dictToSend = {'status': 'GCD'}
        requests.post('http://' + '127.0.0.1' + ':' + str(5000)+ '/soc', json=dictToSend)
        time.sleep(120)
        # con_down = connect_mq(os.environ.get('gcd_listener'))
        # con_down.basic_publish(body=os.environ.get('src_system'), exchange='',routing_key=os.environ.get('gcd_listener'))

    channel.basic_consume(queue=os.environ.get('gcd_listener'), auto_ack=True, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__=='__main__':
    p1= mp.Process(target=upstream_listner)
    p2= mp.Process(target=downstream_listner)
    p3= mp.Process(target=gcd_listner)
    p1.start()
    p2.start()
    p3.start()























    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    # channel = connection.channel()
    # channel.queue_declare(queue=os.environ.get('receiver_queue'),durable=True)
    #
    #
    # def sleep():
    #     time.sleep(120)
    #
    # def callback(ch, method, properties, body):
    #     print('messag received')
    #     dictToSend = {'status': os.environ.get('src_system')}
    #     requests.post('http://'+str(os.environ.get('tracer_ip'))+':'+5000+'/soc', json=dictToSend)
    #     sleep()
    #     if body == 'DOWN':
    #         global connect_gcd
    #         connect_gcd = connect_gcd()
    #         connect_gcd.basic_publish(body=os.environ.get('src_system'), exchange='',routing_key=os.environ.get('gcd_queue'))
    #     else:
    #         global con_down
    #         if con_down == None:
    #             con_down=connect_down_stream()
    #         con_down.basic_publish(body=os.environ.get('src_system'), exchange='', routing_key=os.environ.get('sender_queue'))
    #
    # channel.basic_consume(queue =os.environ.get('receiver_queue'),auto_ack = True,on_message_callback = callback)
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()
    #
    #
    #


