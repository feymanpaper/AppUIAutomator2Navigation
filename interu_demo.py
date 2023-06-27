# coding=utf-8
import threading
import time
import ctypes
import inspect
import asyncio


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            # pass
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)


def stop_thread(thread):
    """终止线程"""
    _async_raise(thread.ident, SystemExit)


class CountdownTask:
    def run(self, n):
        while True:
            # 将要执行的任务放在此处
            # 示例
            print("T-minus  {}\n".format(n))
            n -= 1
            asyncio.sleep(1000)
            # time.sleep(100)
            # end


def terminate_thread(thread):
    if not thread.is_alive():
        print("不活跃？！")
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

if __name__ == '__main__':
    # 示例
    # stop threading
    countdownTask = CountdownTask()
    th = threading.Thread(target=countdownTask.run, args=(10,))  # args可以给run传参
    th.start()
    time.sleep(2)
    terminate_thread(th)  # Signal termination
    time.sleep(1000)
    # end
