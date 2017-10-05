import sys
import uuid
sys.path.append('./')
sys.path.append('../')
import redis
from CiriGateway import CiriGatewayServer
conn=redis.Redis()
guid=''
def sendMessageToGateway(myMessage):
    global guid
    guid=uuid.uuid1().__str__()
    cfg=CiriGatewayServer.GetAllConfig()
    serverListenTo=cfg['listenerQueue']
    consumedMessage=conn.publish(channel=serverListenTo,message=myMessage+":"+guid)
def SubscribeMessageFromServer():
    cfg=CiriGatewayServer.GetAllConfig()
    serverPublishTo=cfg['senderTopic']
    sub=conn.pubsub()
    sub.subscribe(serverPublishTo) 
    while(True):
        for message in sub.listen():
            if(message['type']=='message'):
                myMessage=message['data']
                import CiriUtility.Utility
                messageGuid=CiriUtility.Utility.GetMessageGUID(myMessage.decode('utf-8'))
                global guid
                if(messageGuid==guid):
                    print(CiriUtility.Utility.GetMessageContent(message['data'].decode('utf-8')))

