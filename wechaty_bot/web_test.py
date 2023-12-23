# bot.py
from wechaty import Wechaty
import os
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='192.168.0.107:7891'
os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='968e1180-d977-4826-97fa-6784203d03c6'
import asyncio


async def main():
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print(
        'Scan QR Code to login: {}\nhttps://wechaty.js.org/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logged in'.format(user)))
    bot.on('message', lambda message: print('Message: {}'.format(message)))
    await bot.start()


asyncio.run(main())