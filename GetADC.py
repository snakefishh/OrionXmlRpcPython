
from threading import Thread
import time

import telebot
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client


from telebot import apihelper
apihelper.proxy = {'http':'http://proxy.azot.kmr:3128'}
apihelper.API_URL = "http://46.181.26.73/bot{0}/{1}"

api_token = '5820420595:AAEkPAGtRi-GED2eh4uPoSv8mCzkwaY1_Ks'
chat_id   = '318983573'
host_orion={'ip':'10.77.19.241', 'port':'8080'}
host_xml_server={'ip':'10.77.19.188', 'port':11111}


bot = telebot.TeleBot(api_token)

s = xmlrpc.client.ServerProxy('http://'+host_orion['ip']+':'+host_orion['port'])
GUID_client={}
GUID_client=s.SetSubscribe({'LOGIN': 'ADMINISTRATOR', 'PASSWORD': 'ORION', 'SCRIBE': 65535, 'SCRIBEPORTS': 'SCRIBEALLPORTS'})\
    .get('RESULTDATA').get('GUID')

class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/xml-rpc',)

def XMLRPC():
    def AnswerADC(data):
 
        addr=data['Comment'].split('/')
        
        rec={'GUID':GUID_client,
        'ZONES':{'ADDRESS':[]}       
        }
        
        dataForGet={
                'ADDRELEMENT':int(addr[3]),
                'ADDRDEVICE':int(addr[2]),
                'ADDRPULT':int(addr[1]),
                'ADDRPORT':int(addr[0])
            }
        rec['ZONES']['ADDRESS'].append(dataForGet)

        state = s.GetStateElements(rec)['RESULTDATA']['STATEZONES'][0]['NAMESTATE']
        
        mess=data['Comment']+'\n'+state+'\n'+'ADCReal: '+str(data['ADCReal'])+'\n'+'ADCValue: '+str(data['ADCValue'])+'\n'+'Value: '+str(data['Value'])
        bot.send_message(chat_id, mess)

        print(mess)

        return('OK')
    
    OrionXMLRPCServer= SimpleXMLRPCServer((host_xml_server['ip'], host_xml_server['port']), requestHandler=RequestHandler)
    OrionXMLRPCServer.register_function(AnswerADC, 'AnswerADC')
    OrionXMLRPCServer.serve_forever()

def Telegram():

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        addr = message.text.split()
        #addr = message.split()

        dev=s.GetDeviceList()

        #Получение ID по Адресу
        #addr=[15,0,4,4]
        id=0
        for comPort in dev['ComPortList']:                                    #Порт
            if comPort['ComPort']==int(addr[0]):   
                for MdevList in comPort['DeviceList']:
                    if MdevList['DeviceAddress']==int(addr[1]):                #Пульт
                        for devList in MdevList['DeviceList']:
                            if devList['DeviceAddress']==int(addr[2]):         #Устройство
                                for ShleifList in devList['ShleifList']:
                                    if ShleifList['Address'] ==int(addr[3]):    #Шлейф
                                        id=ShleifList['ID']

        
        if id ==0:
            bot.send_message(chat_id, 'Нет Такого Устройства')
        else:
            rec={'IPSERVER':host_xml_server['ip'], 'PORTSERVER':host_xml_server['port'], 'MethodNameForAnswer':'AnswerADC', 'ReturnHandle':0}
            print(s.GetADCOfZone( rec, id))

        
    bot.polling(none_stop=True, interval=0)
    #get_text_messages('17 1 12 5')


if __name__ == '__main__':

    # th_XMLRPC = Thread(target=XMLRPC)
    # th_XMLRPC.daemon=True
    # th_XMLRPC.start()

    # th_Telegram = Thread(target=Telegram)
    # th_Telegram.daemon=True
    # th_Telegram.start()
    Telegram()







    while input()!='q':
        time.sleep(1)

    print('END')

 