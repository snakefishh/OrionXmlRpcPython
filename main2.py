import asyncio
from aiosmtpd.controller import Controller
from urllib.parse import unquote

class ExampleHandler:
    #  async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
    #      if not address.endswith('@example.com'):
    #          return '550 not relaying to that domain'
    #      envelope.rcpt_tos.append(address)
    #      return '250 OK'

     async def handle_DATA(self, server, session, envelope):
         print('Message from %s' % envelope.mail_from)
         print('Message for %s' % envelope.rcpt_tos)
         print('Message data:\n')
         for ln in envelope.content.decode('1251', errors='replace').splitlines():
             #ln1=unquote(ln.decode('1251'))
             print(f'> {ln}'.strip())
         print()
         print('End of message')
         return '250 Message accepted for delivery'






def run():
    controller = Controller(ExampleHandler(), hostname="", port=25)
    controller.start()
    input("Server started. Press Return to quit.")
    controller.stop()

if __name__ == '__main__':
    print('#################################')
    run()