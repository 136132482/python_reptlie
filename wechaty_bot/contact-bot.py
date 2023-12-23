"""doc"""
import asyncio
from typing import Optional

from wechaty_puppet import ContactType
from wechaty_puppet.logger import get_logger
from wechaty.user import Message, Room

from wechaty import Wechaty, Contact
from wechaty.utils.qrcode_terminal import qr_terminal_str
import os
os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='puppet_padlocal_8016548d2b554ebbb4f5c89767a83b00'
os.environ['WECHATY_PUPPET']='wechaty-puppet-padlocal'
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='192.168.0.107:7890'
log = get_logger('ContactBot')

WELCOME_MSG = '''
=============== Powered by Wechaty ===============
-------- https://github.com/Chatie/wechaty --------
Hello,
I'm a Wechaty Botie with the following super powers:
1. List all your contacts with weixn id & name
2. Dump the avatars of your first 17 contacts
__________________________________________________
Hope you like it, and you are very welcome to
upgrade me for more super powers!
Please wait... I'm trying to login in...
'''

# pylint: disable=W0602
bot: Optional[Wechaty] = None
MAX_CONTACTS = 17
INTERVAL = 7


async def display_contacts() -> None:
    """Display all the contacts and dump the avatars"""
    # pylint: disable=W0603
    global bot
    assert bot is not None
    while True:
        contacts = await bot.Contact.find_all()

        log.info('#######################')
        log.info('Contact number: %s\n', len(contacts))

        for index, contact in enumerate(contacts):
            if contact.type() == ContactType.CONTACT_TYPE_PERSONAL:
                #如果是公众号就不要
                if contact.is_offical():
                   contacts.remove(contact)
                if contact.name =='':
                    contacts.remove(contact)
                if contact.is_self():
                    contacts.remove(contact)
                log.info('当前联系人是： %s: %s : %s', index, contact.name, contact.get_id())


        for contact in contacts[:MAX_CONTACTS]:
            file = await contact.avatar()
            name = file.name
            await file.to_file(name, True)
            await contact.say("微信测试，不需回复")
            log.info('联系人: "%s" with avatar file: "%s"', contact.name, name)

        if len(contacts) > MAX_CONTACTS:
            log.info('Too many contacts. I only show you the first %s ones...', MAX_CONTACTS)

        log.info('I will re-dump contact weixin id & names after %s second... ', INTERVAL)
        await asyncio.sleep(INTERVAL)


async def handle_login(user: Contact) -> None:
    """Handle the login event"""
    log.info('%s logged in', user.name)
    await user.say('wechaty contact-bot just logged in')
    await display_contacts()


async def main() -> None:
    """The main function for the contact-bot module"""
    # pylint: disable=W0603
    global bot
    print(WELCOME_MSG)
    bot = Wechaty()\
        .on('login', handle_login)\
        .on('error', lambda error: log.info('error: %s', error))\
        .on('scan',
            lambda qrcode, status: print(f'{qr_terminal_str(qrcode)}\n'
                                         f'[{status}] Scan QR Code in above url to login:'))
    await bot.start()


asyncio.run(main())
