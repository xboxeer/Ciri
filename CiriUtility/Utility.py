import re
def GetMessageContent(message):
    return re.findall('[^.]*(?=:[^:]*$)',message)[0]
def GetMessageGUID(message):
    return re.findall('[^:]*$',message)[0]
import configparser
def GetAllConfig():
    cfg=configparser.ConfigParser()
    if(cfg.read('../CiriSetting.cfg').count('../CiriSetting.cfg')==0):
        cfg.read('./CiriSetting.cfg')
    topicName=cfg.get('gatewaySenderTopic','name')
    queueName=cfg.get('gatewayListenerQueue','name')
    redisServer=cfg.get('redisServer','name')
    redisServerPort=cfg.get('redisServer','port')
    return {'GatewaySenderTopic':topicName,'GatewayListenerQueue':queueName,'redisServer ':redisServer,\
'redisServerPort':redisServerPort}