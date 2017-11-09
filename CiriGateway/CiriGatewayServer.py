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
    from chatterbot import ChatBot
    ciri=ChatBot('Ciri',logic_adapters=["chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter",
        {"import_path": "chatterbot.logic.BestMatch",
         "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
         "response_selection_method": "chatterbot.response_selection.get_first_response"}])
    from chatterbot.trainers import ListTrainer
    conversion=[
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."]
    ciri.set_trainer(ListTrainer)
    ciri.train(conversion)
    if(message == 'Hello Ciri'):
        print('Hit, replying')
        returnMessage='Hello'
    else:
        returnMessage=ciri.get_response(message).text
        #print('Not hit')
        #returnMessage="Sorry I don't understand"
    returnMessage=returnMessage+":"+guid
    replyQueue.put(returnMessage)
