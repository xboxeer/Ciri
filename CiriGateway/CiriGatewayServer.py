import sys
import multiprocessing as mp
sys.path.append('./')
sys.path.append('../')
import configparser
def GetAllConfig():
    cfg=configparser.ConfigParser()
    if(cfg.read('../CiriSetting.cfg').count('../CiriSetting.cfg')==0):
        cfg.read('./CiriSetting.cfg')
    topicName=cfg.get('gatewaySenderTopic','name')
    queueName=cfg.get('gatewayListenerQueue','name')
    redisServer=cfg.get('redisServer','name')
    redisServerPort=cfg.get('redisServer','port')
    return {'senderTopic':topicName,'listenerQueue':queueName,'redisServer ':redisServer,\
'redisServerPort':redisServerPort}
import redis
import queue
import threading
replyQueue=queue.Queue()
def StartServer():
    replyThread=threading.Thread(target=SendMessageBack,daemon=True)
    replyThread.start()
    cfg=GetAllConfig()
    conn=redis.Redis(host='localhost')
    sub=conn.pubsub()
    listenTo=cfg['listenerQueue']
    publishTo=cfg['senderTopic']
    sub.subscribe(listenTo)
    print('Start Listening')
    for message in sub.listen():
        if(message['type']=='message'):
            RouteToNLTKProcessor(message['data'])
def SendMessageBack():
    cfg=GetAllConfig()
    topicName=cfg['senderTopic']
    conn=redis.Redis(host='localhost')
    while(True):
        replyMessage=replyQueue.get(block=True)
        pub=conn.publish(topicName,replyMessage)
def RouteToNLTKProcessor(message):
    returnMessage=''
    import sys
    sys.path.append('./')
    sys.path.append('../')
    import CiriUtility.Utility
    guid=CiriUtility.Utility.GetMessageGUID(message.decode('utf-8'))
    message=CiriUtility.Utility.GetMessageContent(message.decode('utf-8'))
    if(message == 'Hello Ciri'):
        print('Hit, replying')
        returnMessage='Hello'
    else:
        print('Not hit')
        returnMessage="Sorry I don't understand"
    returnMessage=returnMessage+":"+guid
    replyQueue.put(returnMessage)
