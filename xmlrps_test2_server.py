


def server():
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.server import SimpleXMLRPCRequestHandler
    import xmlrpc.client
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/xml-rpc',)

    def AnswerADC(data):
        print(data)
        return('OK')
	
    def ONCHANGESTATEELEMENTS(data):
        print(data)
        return('OK')
   
    s = xmlrpc.client.ServerProxy('http://192.168.0.107:8080')

    GUID={}
    GUID=s.SetSubscribe({'LOGIN': 'ADMINISTRATOR', 'PASSWORD': 'ORION', 'SCRIBE': 65535, \
        'IPSERVER':'192.168.0.2', 'PORTSERVER':1111,\
        'SCRIBEPORTS': 'SCRIBEALLPORTS'})\
        .get('RESULTDATA').get('GUID')
    
    server = SimpleXMLRPCServer(("192.168.0.2", 1111), requestHandler=RequestHandler)
    server.register_function(AnswerADC, 'AnswerADC')
    server.register_function(ONCHANGESTATEELEMENTS, 'ONCHANGESTATEELEMENTS')

    server.serve_forever()

if __name__ == '__main__':
    server()