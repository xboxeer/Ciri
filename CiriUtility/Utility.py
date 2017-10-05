import re
def GetMessageContent(message):
    return re.findall('[^.]*(?=:[^:]*$)',message)[0]
def GetMessageGUID(message):
    return re.findall('[^:]*$',message)[0]