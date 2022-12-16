from datetime import datetime
import asyncore
from smtpd import SMTPServer
from urllib.parse import urlencode
from urllib.parse import unquote

class EmlServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print('-----------------')
        print(unquote(data.decode('1251')))


def run():
    EmlServer(('0.0.0.0', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    print('#################################')
    run()