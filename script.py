
# SuperFastPython.com
# example of running a blocking function call in asyncio in a new thread
import time
import asyncio
 
# blocking function
def blocking_task():
    while True:
        # report a message
        print('task is running')
        user_input = input("\nINPUT HERE\n")
        print('INPUT HERE', user_input)
        # block
        time.sleep(2)
        # report a message
    print('task is done')
 
# background coroutine task
async def background():
    # loop forever
    while True:
        # report a message
        print('>background task running')
        # sleep for a moment
        await asyncio.sleep(0.5)
 
# main coroutine
async def main():
    # run the background task
    _= asyncio.create_task(background())
    # create a coroutine for the blocking function call
    coro = asyncio.to_thread(blocking_task)
    # execute the call in a new thread and await the result
    await coro
 
# start the asyncio program
asyncio.run(main())