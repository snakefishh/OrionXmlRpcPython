
def client():
    import xmlrpc.client
    
    s = xmlrpc.client.ServerProxy('http://192.168.0.106:8080')
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
    s = xmlrpc.client.ServerProxy('http://192.168.0.107:8080')
    #print (s.system.listMethods())
    GUID={}
    GUID=s.SetSubscribe({'LOGIN': 'ADMINISTRATOR', 'PASSWORD': 'ORION', 'SCRIBE': 65535, 'SCRIBEPORTS': 'SCRIBEALLPORTS'})\
         .get('RESULTDATA').get('GUID') 
    rec={'GUID':GUID}
    
    #print(s.GetDeviceList())
    dev=s.GetListDevice(rec)
    #print(dev)
    #print(s.GetListRsCommand(rec))

    print(dev['RESULTDATA']['DEVICES'][0]['ZONES'][0]['NAMESTATE'])



def run():
    import xmlrpc.client
    s = xmlrpc.client.ServerProxy('http://192.168.0.2:8080')

    # GUID={}
    # GUID=s.SetSubscribe({'LOGIN': 'ADMINISTRATOR', 'PASSWORD': 'ORION', 'SCRIBE': 65535, 'SCRIBEPORTS': 'SCRIBEALLPORTS'})\
    #     .get('RESULTDATA').get('GUID')

    rec={'IPSERVER':'192.168.0.2', 'PORTSERVER':1111, 'MethodNameForAnswer':'AnswerADC', 'ReturnHandle':0}

    s.GetADCOfZone( rec, 5)
    print(s.GetADCOfZone( rec, 5))

   # server()


if __name__ == '__main__':
    #run()
    #client()
    getDevices()
