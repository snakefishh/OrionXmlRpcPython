def client():
    import xmlrpc.client
    
    s = xmlrpc.client.ServerProxy('http://192.168.0.2:8080')
    print (s.system.listMethods())
    GUID={}
    GUID=s.SetSubscribe({'LOGIN': 'ADMINISTRATOR', 'PASSWORD': 'ORION', 'SCRIBE': 65535, 'SCRIBEPORTS': 'SCRIBEALLPORTS'})\
        .get('RESULTDATA').get('GUID')
    rec={'GUID':GUID,
        'ZONES':{'ADDRESS':[]}       
        }
    
    data={
            'ADDRELEMENT':235,
            'ADDRDEVICE':188,
            'ADDRPULT':74,
            'ADDRPORT':110
        }
    rec['ZONES']['ADDRESS'].append(data)
    print(s.GetStateElements(rec))


def getDevices():
    import xmlrpc.client
    s = xmlrpc.client.ServerProxy('http://192.168.0.2:8080')
    #print (s.system.listMethods())
    GUID={}
    GUID=s.SetSubscribe({'LOGIN': 'ADMINISTRATOR', 'PASSWORD': 'ORION', 'SCRIBE': 65535, 'SCRIBEPORTS': 'SCRIBEALLPORTS'})\
         .get('RESULTDATA').get('GUID')
    rec={'GUID':GUID}
    
    #print(s.GetDeviceList())
    dev=s.GetListDevice(rec)
    print(dev)
    #print(s.GetListRsCommand(rec))

    print(dev['RESULTDATA']['DEVICES'][0]['ZONES'][1]['NAMESTATE'])






    
from threading import Thread

def server():
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.server import SimpleXMLRPCRequestHandler
    import xmlrpc.client
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/xml-rpc',)

    def AnswerADC(data):
        print('-----------AnswerADC---------------')
        print(data)
        return('OK')
	
    def ONCHANGESTATEELEMENTS(data):
        print('-----------ONCHANGESTATEELEMENTS---------------')
        print(data)
        return('OK')

    def ONRSEVENT(data):
        print('-----------ONRSEVENT---------------')
        print(data)
        return('OK')
   
    s = xmlrpc.client.ServerProxy('http://192.168.0.2:8080')

    GUID={}
    GUID=s.SetSubscribe({'LOGIN': 'ADMINISTRATOR', 'PASSWORD': 'ORION', 'SCRIBE': 65535, \
        'IPSERVER':'192.168.0.2', 'PORTSERVER':1111,\
        'SCRIBEPORTS': 'SCRIBEALLPORTS'})\
        .get('RESULTDATA').get('GUID')
    
    server = SimpleXMLRPCServer(("192.168.0.2", 1111), requestHandler=RequestHandler)
    server.register_function(AnswerADC, 'AnswerADC')
    server.register_function(ONCHANGESTATEELEMENTS, 'ONCHANGESTATEELEMENTS')
    server.register_function(ONRSEVENT, 'ONRSEVENT')

    server.serve_forever()

if __name__ == '__main__':
    th = Thread(target=server)
    th.start()