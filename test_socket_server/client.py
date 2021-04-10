import asyncio
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('connection established')


@sio.event
async def update_game(data):
    print('message received with ', data)


@sio.event
async def disconnect():
    print('disconnected from server')


async def main():
    await sio.connect('http://127.0.0.1:443')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())