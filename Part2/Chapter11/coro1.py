import uasyncio
import time

async def coro2():
    print("coro2 start")
    await coro2x()
    print("coro2 end")
        
async def coro2x():
    print("coro2x start")
    # 1秒間かかる処理が行われていることをシミュレートする。
    time.sleep(1)
    print("coro2x end")

async def coro3():
    print("coro3 start")
    await uasyncio.sleep(10)
    print("coro3 end")
        
async def coro1():
    print("coro1 start")
    task2 = uasyncio.create_task(coro2())
    task3 = uasyncio.create_task(coro3())
    print("await coro2")
    await task2
    print("await coro3")
    await task3
    print("coro1 end")
    
uasyncio.run(coro1())
print("all done")
