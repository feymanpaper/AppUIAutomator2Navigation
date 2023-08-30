import threading, time
from queue import Queue

# Producer thread
class Producer(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):  # 随机产生10个数字 ，可以修改为任意大小
            print("%s: %s is producing %d to the queue!" % (time.ctime(), self.name, i))
            self.data.put(i)  # 将数据依次存入队列
        print("%s: %s finished!" % (time.ctime(), self.name))


# Consumer thread
class Consumer_even(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        while 1:
            try:
                val_even = self.data.get(1, 5)  # get(self, block=True, timeout=None) ,1就是阻塞等待,5是超时5秒
                if val_even % 2 == 0:
                    print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.name, val_even))
                    time.sleep(2)
                else:
                    self.data.put(val_even)
                    time.sleep(2)
            except:  # 等待输入，超过5秒  就报异常
                print("%s: %s finished!" % (time.ctime(), self.name))
                break

class Consumer_odd(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        while 1:
            try:
                val_odd = self.data.get(1, 5)
                if val_odd % 2 != 0:
                    print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.name, val_odd))
                    time.sleep(2)
                else:
                    self.data.put(val_odd)
                    time.sleep(2)
            except:
                print("%s: %s finished!" % (time.ctime(), self.name))
                break

# Main thread
def main():
    queue = Queue()
    producer = Producer('Pro.', queue)
    consumer_even = Consumer_even('Con_even.', queue)
    consumer_odd = Consumer_odd('Con_odd.', queue)
    producer.start()
    consumer_even.start()
    consumer_odd.start()
    producer.join()
    consumer_even.join()
    consumer_odd.join()
    print('All threads terminate!')

if __name__ == '__main__':
    main()