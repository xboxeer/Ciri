import sys
sys.path.append('./')
sys.path.append('../')
import mockClient
import threading
thread=threading.Thread(target=mockClient.SubscribeMessageFromServer,daemon=True)
thread.start()
while(True):
    myInput=input()
    mockClient.sendMessageToGateway(myInput)