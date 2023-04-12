
from multiprocessing import Process
import time

def main():
    gpsCoor = 123.23
    p = Process(target=testWrite,args=())
    p.start()
    #time.sleep(5)
    #p.terminate()
    #print('done')


def testWrite():
    t = time.time()
    while True:
        if time.time()-t>1:
            t = time.time()
            with open("testTXT.txt") as f:
                lines = f.read().splitlines()
                if len(lines)>=10:
                    lines=lines[1:]
                gpsCoor = str(time.time())
            with open("testTXT.txt", 'w') as f:
                for line in lines:
                    f.write(line+'\n')
                f.write(gpsCoor+'\n')

if __name__ == '__main__':
    main()