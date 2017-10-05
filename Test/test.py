import sys
sys.path.append('./')
sys.path.append('../')
from CiriGateway import CiriGatewayServer
result=CiriGatewayServer.GetAllConfig()
CiriGatewayServer.StartServer()
