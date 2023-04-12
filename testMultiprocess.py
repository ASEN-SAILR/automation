from multiprocessing import Process, Value, Array
import time
from datetime import datetime
import pytz
import numpy as np

# class testSharedMemory():
#     def __init__(self):
#         self.var = Value('i', True)
#         self.var.value = 0
#     def startChild(self):
#         p = Process(target=self.child, args=(self.var))
#         p.start()
#     def child(self,value):
#         value = 1

# if __name__ == '__main__':
#     test = testSharedMemory()
#     print('before child overwrite: ',test.var.value)
#     test.startChild()
#     time.sleep(.1)
#     print('after child overwrite: ',test.var.value)

class testSharedMemory():
    def __init__(self):
        self.var = Value('b', True)
        self.arr = Array('f', np.zeros(3*2*2))
        # self.arr = np.reshape(self.arr, (2, 5))
    def startChild(self):
        p = Process(target=self.child, args=(self.var,self.arr))
        p.daemon = True
        p.start()
    def child(self, var, arr):
        var.value = False
        frame = np.array([[[1,2],[3,4]],[[5,6],[7,8]],[[9,10],[11,12]]])
        arr[:] = frame.flatten()

if __name__ == '__main__':
    test = testSharedMemory()
    print('before child overwrite: var=',test.var.value)
    print('before child overwrite: arr=',np.array((test.arr)))
    test.startChild()
    time.sleep(1)
    print('after child overwrite: var=',test.var.value)
    x = np.array(test.arr).reshape(2,2,3)
    print('after child overwrite: arr=',x)
    print('shape',x.shape)














