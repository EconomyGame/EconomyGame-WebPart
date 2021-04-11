import asyncio
import socketio
import sys

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
    while True:
        await sio.connect('http://tp-project2021.herokuapp.com')
        await sio.wait()

if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except Exception as D:
            sys.stderr.write("Connection Runtime Error\n")
