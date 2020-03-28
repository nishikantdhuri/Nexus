import multiprocessing as mp
import pika
import time
import os
con_down=None
con_gcd=None
import requests
folder = os.path.dirname(os.path.abspath(__file__))
folder = folder + '\logs'

def connect_mq(mq):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host'),heartbeat=120))
    channel = connection.channel()
    channel.queue_declare(queue=mq, durable=True)
    return channel

def upstream_listner():
    import logging
    logging.basicConfig(filename=os.path.join(folder, 'up.log'), filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info('connecting to mq ' + str(os.environ.get('receiver_queue')))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('receiver_queue'), durable=True)

    def callback(ch, method, properties, body):
        logging.info('messag received')
        dictToSend = {'status': os.environ.get('src_system')}
        requests.post('http://'+str(os.environ.get('tracer_ip'))+':'+str(5000)+'/soc', json=dictToSend)
        logging.info('Processing...')
        time.sleep(int(os.environ.get('sleep_time')))
        logging.info('Process completed')
        logging.info('Sending message to '+ str(os.environ.get('downstream_sender')) + 'from '+str(os.environ.get('src_system')))
        con_down=connect_mq(os.environ.get('downstream_sender'))
        con_down.basic_publish(body=os.environ.get('src_system'), exchange='', routing_key=os.environ.get('downstream_sender'))
        con_down.close()

    channel.basic_consume(queue = os.environ.get('receiver_queue'),auto_ack = True,on_message_callback = callback)
    logging.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def downstream_listner():
    import logging
    logging.basicConfig(filename=os.path.join(folder, 'down.log'), filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info('connecting to mq ' + str(os.environ.get('downstream_listener')))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('downstream_listener'), durable=True)

    def callback(ch, method, properties, body):
        logging.info('messag received')
        dictToSend = {'status': os.environ.get('src_system')}
        requests.post('http://' + str(os.environ.get('tracer_ip')) + ':' + str(5000) + '/soc', json=dictToSend)
        logging.info('Processing...')
        time.sleep(int(os.environ.get('sleep_time')))
        logging.info('Process completed')
        logging.info('Sending message to ' + str(os.environ.get('gcd_sender')) + 'from ' + str(
            os.environ.get('src_system')))
        con_down = connect_mq(os.environ.get('gcd_sender'))
        con_down.basic_publish(body=os.environ.get('src_system'), exchange='',routing_key=os.environ.get('gcd_sender'))
        con_down.close()

    channel.basic_consume(queue=os.environ.get('downstream_listener'), auto_ack=True, on_message_callback=callback)
    logging.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def gcd_listner():
    import logging
    logging.basicConfig(filename=os.path.join(folder, 'gcd.log'), filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info('connecting to mq ' + str(os.environ.get('gcd_listener')))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host')))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('gcd_listener'), durable=True)

    def callback(ch, method, properties, body):
        logging.info('messag received')
        dictToSend = {'status': os.environ.get('src_system')}
        logging.info('Processing...')
        requests.post('http://' + str(os.environ.get('tracer_ip')) + ':' + str(5000)+ '/soc', json=dictToSend)
        time.sleep(int(os.environ.get('sleep_time')))
        logging.info('Process complete')

    channel.basic_consume(queue=os.environ.get('gcd_listener'), auto_ack=True, on_message_callback=callback)
    logging.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__=='__main__':
    #import os
    # os.environ['receiver_queue']='upstream'
    # os.environ['downstream_sender'] = 'downstream1'
    # os.environ['downstream_listener'] = 'downstream2'
    # os.environ['gcd_sender'] = 'gcd1'
    # os.environ['gcd_listener'] = 'gcd2'
    # os.environ['src_system'] = 'nexus'
    # os.environ['mq_host'] = '192.168.99.100'
    # os.environ['tracer_ip'] = '127.0.0.1'
    # os.environ['sleep_time']='60'
    p1= mp.Process(target=upstream_listner)
    p2= mp.Process(target=downstream_listner)
    p3= mp.Process(target=gcd_listner)
    p1.start()
    p2.start()
    p3.start()