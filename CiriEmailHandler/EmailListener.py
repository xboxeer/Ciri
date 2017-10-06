import sys
sys.path.append('./')
sys.path.append('../')
import imaplib
import email
import configparser
import CiriGateway.CiriGatewayUtility
import threading
messagesToBeSend=dict()
ciriMailbox=''
ciriMailboxPwd=''
ciriSmtpServer=''
def __SendMail(message,messageGUID):
    global ciriMailbox
    global ciriMailboxPwd
    global ciriSmtpServer
    item=messagesToBeSend.pop(messageGUID)
    print(item["subject"])
    print(item["mailfrom"])
    print(item["content"])
    print(message)
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    mailContent=MIMEText(message,'plain','utf-8')
    mailContent['From']=ciriMailbox
    mailContent['To']=item['mailfrom']
    mailContent['Subject']=Header('re:'+item['subject'],'utf-8')
    smtpServer=smtplib.SMTP(ciriSmtpServer)
    smtpServer.login(ciriMailbox,ciriMailboxPwd)
    smtpServer.sendmail(ciriMailbox,item["mailfrom"],mailContent.as_string())
def StartEmailMonitor():
    cfg=configparser.ConfigParser()
    if(cfg.read('../CiriSetting.cfg').count('../CiriSetting.cfg')==0):
        cfg.read('./CiriSetting.cfg')
    global ciriSmtpServer
    global ciriMailbox
    global ciriMailboxPwd
    cfgDict=dict(cfg.items(section='ciriMailbox'))
    conn=imaplib.IMAP4_SSL(cfgDict['imap_server'])
    ciriSmtpServer=cfgDict['smtp_server']
    ciriMailbox=cfgDict['address']
    ciriMailboxPwd=cfgDict['password']
    conn.login(cfgDict['address'],cfgDict['password'])
    while(True):
        import time
        time.sleep(5)
        conn.select()
        result,messageIndex=conn.search(None,'Unseen')
        for item in messageIndex[0].split():
            result,items=conn.fetch(item,('RFC822'))
            mailText=items[0][1]
            mailMessage=email.message_from_bytes(mailText)
            mailContent=''
            if(mailMessage.is_multipart()):
                for mail in mailMessage.get_payload():
                    if(mail['Content-Type'].find('plain')>0):
                        payload=mail.get_payload(decode=True).decode()
                        header=email.header.decode_header(mailMessage['Subject'])[0]
                        subject=header[0].decode(header[1])
                        mailFrom=mailMessage['From']
                        message,guid=CiriGateway.CiriGatewayUtility.SendMessageToGateway(payload.strip())
                        messagesToBeSend[guid]={'subject':subject,'mailfrom':mailFrom,'content':message}
            else:
                mailContent=mailMessage['Content-Type']
        pass
subThread=threading.Thread(target=CiriGateway.CiriGatewayUtility.SubscribeMessageFromServer,args=(__SendMail,))
subThread.start()
emailMonitorThread=threading.Thread(target=StartEmailMonitor,daemon=True)
emailMonitorThread.start()
emailMonitorThread.join()
